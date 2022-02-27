from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.schemas.user_schema import UserSignUp, User
from app.auth import get_password_hash
from app.crud.user_data import add_user


def add_new_user(user: UserSignUp, db: Session) -> User:
    user.password = get_password_hash(user.password)
    try:
        new_user = add_user(db, user)
    except IntegrityError as e:

        raise HTTPException(status_code=409, detail="Username or email already "
                                                    "exists")
    return new_user
