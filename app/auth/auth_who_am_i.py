from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserFullData

from app.crud.user_data import get_user_by_id


def get_user_from_jwt_data(db: Session, Authorize: AuthJWT) -> UserFullData:
    user_db = get_user_by_id(db, Authorize.get_jwt_subject())
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db
