from datetime import datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RouterCreate(BaseModel):
    hotel_id: int
    name: str
    host: str
    api_port: int = 8728
    username: str
    password: str
    hotspot_server: str | None = None


class RouterRead(BaseModel):
    id: int
    hotel_id: int
    name: str
    host: str
    api_port: int
    hotspot_server: str | None = None
    active: bool

    class Config:
        from_attributes = True


class CaptiveLoginRequest(BaseModel):
    hotel_slug: str
    room_number: str | None = None
    last_name: str | None = None
    voucher_code: str | None = None


class StaySyncPayload(BaseModel):
    room_number: str
    first_name: str
    last_name: str
    voucher_code: str | None = None
    check_in_at: datetime
    check_out_at: datetime
    login_mode: str = "room_lastname"
