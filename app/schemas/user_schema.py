from typing import Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserSignUp(BaseModel):
    username: str = Field(..., min_length=4, max_length=30)
    email: EmailStr = Field(...)
    password: str


class UserSignIn(BaseModel):
    username: Union[EmailStr, str]


class UserPassword(UserSignIn):
    password: str


class UserValidation(UserSignIn):
    validated: bool
    validate_time: Any
    password: str


class User(UserSignIn):
    id: int
    active: bool
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class UserFullData(User, UserSignUp):

    creation_time: datetime
    validated: bool
    validate_time: Any

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    name: str
    surname: str
    birthday: str


class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class LoginToken(AccessToken, RefreshToken):
    pass


class VerifyTokens(BaseModel):
    token: str


class RestorePwdEmail(BaseModel):
    email: str


class NewPassword(VerifyTokens):
    password: str
    restore_mail_token: str
