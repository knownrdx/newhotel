from datetime import datetime, timedelta

from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models.models import GuestStay, Hotel, RoomPolicy, StaffUser


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        hotel = db.query(Hotel).filter_by(slug="demo-hotel").first()
        if not hotel:
            hotel = Hotel(
                name="Demo Hotel",
                slug="demo-hotel",
                welcome_message="Welcome to Demo Hotel WiFi",
                primary_color="#0f766e",
                supported_languages=["en", "bn"],
                subscription_plan="starter",
            )
            db.add(hotel)
            db.flush()

        staff = db.query(StaffUser).filter_by(email="admin@demo.local").first()
        if not staff:
            staff = StaffUser(
                hotel_id=hotel.id,
                email="admin@demo.local",
                full_name="Demo Admin",
                password_hash=hash_password("admin123"),
                is_super_admin=True,
            )
            db.add(staff)

        policy = db.query(RoomPolicy).filter_by(hotel_id=hotel.id, room_number="101").first()
        if not policy:
            db.add(RoomPolicy(
                hotel_id=hotel.id,
                room_number="101",
                max_devices=3,
                bandwidth_up_kbps=10000,
                bandwidth_down_kbps=10000,
                session_timeout_minutes=720,
            ))

        stay = db.query(GuestStay).filter_by(hotel_id=hotel.id, room_number="101", last_name="Park").first()
        if not stay:
            db.add(GuestStay(
                hotel_id=hotel.id,
                pms_reservation_id="DEMO-RES-001",
                room_number="101",
                first_name="Ji-hoon",
                last_name="Park",
                voucher_code="DEMO101",
                check_in_at=datetime.utcnow() - timedelta(hours=1),
                check_out_at=datetime.utcnow() + timedelta(days=1),
                wifi_enabled=True,
                login_mode="room_lastname",
            ))

        db.commit()
        print("[OK] Demo data ready")
        print("Hotel slug: demo-hotel")
        print("Admin login: admin@demo.local / admin123")
        print("Portal login: room 101 + Park or voucher DEMO101")
    finally:
        db.close()


if __name__ == "__main__":
    run()
