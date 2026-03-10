from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.security import create_access_token, encrypt_secret, verify_password
from app.db.session import get_db
from app.models.models import GuestStay, Hotel, Router, SessionLog, StaffUser
from app.schemas.schemas import CaptiveLoginRequest, LoginRequest, RouterCreate
from app.services.guest_access import GuestAccessService

router = APIRouter(prefix="/api")


@router.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(StaffUser).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token(user.email), "token_type": "bearer"}


@router.post("/routers")
def create_router(payload: RouterCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = Router(
        hotel_id=payload.hotel_id,
        name=payload.name,
        host=payload.host,
        api_port=payload.api_port,
        username=payload.username,
        password_encrypted=encrypt_secret(payload.password),
        hotspot_server=payload.hotspot_server,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    hotel_id = user.hotel_id
    active_guests = db.query(func.count(GuestStay.id)).filter_by(hotel_id=hotel_id, wifi_enabled=True).scalar()
    online_sessions = db.query(func.count(SessionLog.id)).filter_by(hotel_id=hotel_id, status="online").scalar()
    total_bandwidth = db.query(func.coalesce(func.sum(SessionLog.bytes_in + SessionLog.bytes_out), 0)).filter_by(hotel_id=hotel_id).scalar()
    return {
        "active_guests": active_guests,
        "online_sessions": online_sessions,
        "bandwidth_bytes": total_bandwidth,
    }


@router.get("/guests/online")
def online_guests(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(SessionLog).filter_by(hotel_id=user.hotel_id, status="online").all()


@router.post("/portal/login")
def captive_login(payload: CaptiveLoginRequest, db: Session = Depends(get_db)):
    service = GuestAccessService()
    stay = service.validate_captive_login(db, payload.hotel_slug, payload.room_number, payload.last_name, payload.voucher_code)
    if not stay or not stay.wifi_enabled:
        raise HTTPException(status_code=401, detail="Invalid guest details or WiFi not active")
    return {"success": True, "room_number": stay.room_number, "guest": f"{stay.first_name} {stay.last_name}"}


@router.get("/hotels/{slug}/branding")
def hotel_branding(slug: str, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter_by(slug=slug).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return {
        "name": hotel.name,
        "logo_url": hotel.logo_url,
        "welcome_message": hotel.welcome_message,
        "primary_color": hotel.primary_color,
        "supported_languages": hotel.supported_languages,
    }
