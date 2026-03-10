from datetime import datetime
from secrets import token_urlsafe
from sqlalchemy.orm import Session
from app.models.models import GuestStay, RoomPolicy, Router, WifiCredential
from app.services.mikrotik import MikroTikService


class GuestAccessService:
    def __init__(self):
        self.mikrotik = MikroTikService()

    def _profile_name(self, hotel_id: int, room_number: str) -> str:
        return f"hotel-{hotel_id}-room-{room_number}"

    def provision_for_stay(self, db: Session, stay: GuestStay):
        policy = db.query(RoomPolicy).filter_by(hotel_id=stay.hotel_id, room_number=stay.room_number).first()
        if not policy:
            policy = RoomPolicy(
                hotel_id=stay.hotel_id,
                room_number=stay.room_number,
                max_devices=3,
                bandwidth_up_kbps=10000,
                bandwidth_down_kbps=10000,
                session_timeout_minutes=720,
            )
            db.add(policy)
            db.flush()

        routers = db.query(Router).filter_by(hotel_id=stay.hotel_id, active=True).all()
        username = f"{stay.room_number}-{stay.last_name.lower()}"
        password = token_urlsafe(8)
        profile_name = self._profile_name(stay.hotel_id, stay.room_number)
        rate = f"{policy.bandwidth_up_kbps}k/{policy.bandwidth_down_kbps}k"
        timeout = f"{policy.session_timeout_minutes}m"

        for router in routers:
            self.mikrotik.ensure_profile(router, profile_name, rate, timeout)
            self.mikrotik.create_hotspot_user(router, username, password, profile_name, shared_users=policy.max_devices)
            db.add(WifiCredential(
                hotel_id=stay.hotel_id,
                stay_id=stay.id,
                router_id=router.id,
                username=username,
                password=password,
                profile_name=profile_name,
                device_limit=policy.max_devices,
                status="active",
            ))

        stay.wifi_enabled = True
        db.commit()
        return {"username": username, "password": password, "device_limit": policy.max_devices}

    def disable_for_stay(self, db: Session, stay: GuestStay):
        credentials = db.query(WifiCredential).filter_by(stay_id=stay.id, status="active").all()
        routers = {r.id: r for r in db.query(Router).filter_by(hotel_id=stay.hotel_id).all()}
        for cred in credentials:
            router = routers.get(cred.router_id)
            if router:
                self.mikrotik.disable_hotspot_user(router, cred.username)
            cred.status = "disabled"
        stay.wifi_enabled = False
        db.commit()

    def validate_captive_login(self, db: Session, hotel_slug: str, room_number: str | None, last_name: str | None, voucher_code: str | None):
        from app.models.models import Hotel
        hotel = db.query(Hotel).filter_by(slug=hotel_slug).first()
        if not hotel:
            return None
        q = db.query(GuestStay).filter(GuestStay.hotel_id == hotel.id, GuestStay.check_out_at > datetime.utcnow())
        if voucher_code:
            stay = q.filter(GuestStay.voucher_code == voucher_code).first()
        else:
            stay = q.filter(GuestStay.room_number == room_number, GuestStay.last_name.ilike(last_name or "")).first()
        return stay
