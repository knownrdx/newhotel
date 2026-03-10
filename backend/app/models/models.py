from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Hotel(Base, TimestampMixin):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    welcome_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    primary_color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    supported_languages: Mapped[dict] = mapped_column(JSON, default=list)
    subscription_plan: Mapped[str] = mapped_column(String(50), default="starter")
    routers = relationship("Router", back_populates="hotel")
    staff = relationship("StaffUser", back_populates="hotel")


class StaffUser(Base, TimestampMixin):
    __tablename__ = "staff_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    hotel = relationship("Hotel", back_populates="staff")


class Router(Base, TimestampMixin):
    __tablename__ = "routers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(String(255))
    host: Mapped[str] = mapped_column(String(255))
    api_port: Mapped[int] = mapped_column(Integer, default=8728)
    username: Mapped[str] = mapped_column(String(255))
    password_encrypted: Mapped[str] = mapped_column(String(1000))
    hotspot_server: Mapped[str | None] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    hotel = relationship("Hotel", back_populates="routers")


class RoomPolicy(Base, TimestampMixin):
    __tablename__ = "room_policies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    room_number: Mapped[str] = mapped_column(String(50))
    max_devices: Mapped[int] = mapped_column(Integer, default=3)
    bandwidth_up_kbps: Mapped[int] = mapped_column(Integer, default=10000)
    bandwidth_down_kbps: Mapped[int] = mapped_column(Integer, default=10000)
    session_timeout_minutes: Mapped[int] = mapped_column(Integer, default=720)
    daily_limit_mb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    __table_args__ = (UniqueConstraint("hotel_id", "room_number", name="uq_room_policy"),)


class GuestStay(Base, TimestampMixin):
    __tablename__ = "guest_stays"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    pms_reservation_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    room_number: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    voucher_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    check_in_at: Mapped[datetime] = mapped_column(DateTime)
    check_out_at: Mapped[datetime] = mapped_column(DateTime)
    wifi_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    login_mode: Mapped[str] = mapped_column(String(30), default="room_lastname")


class WifiCredential(Base, TimestampMixin):
    __tablename__ = "wifi_credentials"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    stay_id: Mapped[int] = mapped_column(ForeignKey("guest_stays.id"))
    router_id: Mapped[int] = mapped_column(ForeignKey("routers.id"))
    username: Mapped[str] = mapped_column(String(80), unique=True)
    password: Mapped[str] = mapped_column(String(120))
    profile_name: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(30), default="active")
    device_limit: Mapped[int] = mapped_column(Integer, default=3)


class SessionLog(Base, TimestampMixin):
    __tablename__ = "session_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    stay_id: Mapped[int | None] = mapped_column(ForeignKey("guest_stays.id"), nullable=True)
    router_id: Mapped[int | None] = mapped_column(ForeignKey("routers.id"), nullable=True)
    username: Mapped[str] = mapped_column(String(80))
    mac_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    device_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    bytes_in: Mapped[int] = mapped_column(Integer, default=0)
    bytes_out: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="online")


class PMSConnection(Base, TimestampMixin):
    __tablename__ = "pms_connections"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    db_type: Mapped[str] = mapped_column(String(20))
    dsn_encrypted: Mapped[str] = mapped_column(String(1200))
    polling_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sync_interval_seconds: Mapped[int] = mapped_column(Integer, default=60)
    mapping: Mapped[dict] = mapped_column(JSON, default=dict)
