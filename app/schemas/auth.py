from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    org_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    org_id: int

    model_config = {"from_attributes": True}


class InviteRequest(BaseModel):
    email: EmailStr
    password: str