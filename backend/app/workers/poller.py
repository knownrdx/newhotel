from time import sleep
from app.db.session import SessionLocal
from app.models.models import PMSConnection, GuestStay
from app.services.guest_access import GuestAccessService
from app.services.pms_sync import PMSSyncService
from datetime import datetime


def run():
    sync = PMSSyncService()
    access = GuestAccessService()
    while True:
        db = SessionLocal()
        try:
            for conn in db.query(PMSConnection).filter_by(polling_enabled=True).all():
                sync.poll_hotel(db, conn)
            expired = db.query(GuestStay).filter(GuestStay.wifi_enabled == True, GuestStay.check_out_at < datetime.utcnow()).all()
            for stay in expired:
                access.disable_for_stay(db, stay)
        finally:
            db.close()
        sleep(60)


if __name__ == "__main__":
    run()
