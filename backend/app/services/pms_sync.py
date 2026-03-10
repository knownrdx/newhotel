from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.core.security import decrypt_secret
from app.models.models import GuestStay, PMSConnection
from app.services.guest_access import GuestAccessService


class PMSSyncService:
    def poll_hotel(self, db: Session, connection: PMSConnection):
        engine = create_engine(decrypt_secret(connection.dsn_encrypted))
        mapping = connection.mapping or {}
        table = mapping.get("table", "reservations")
        sql = mapping.get(
            "sql",
            f"SELECT reservation_id, room_number, first_name, last_name, check_in_at, check_out_at, voucher_code, status FROM {table} WHERE status IN ('checked_in','in_house')"
        )
        access_service = GuestAccessService()
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).mappings().all()
            for row in rows:
                existing = db.query(GuestStay).filter_by(hotel_id=connection.hotel_id, pms_reservation_id=str(row["reservation_id"])).first()
                if not existing:
                    stay = GuestStay(
                        hotel_id=connection.hotel_id,
                        pms_reservation_id=str(row["reservation_id"]),
                        room_number=str(row["room_number"]),
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        voucher_code=row.get("voucher_code"),
                        check_in_at=row["check_in_at"],
                        check_out_at=row["check_out_at"],
                    )
                    db.add(stay)
                    db.flush()
                    access_service.provision_for_stay(db, stay)
