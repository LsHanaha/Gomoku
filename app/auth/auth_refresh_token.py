from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


from app.schemas.user_schema import UserPassword, RefreshToken, UserFullData, \
    AccessToken

from app.crud.user_data import get_user
import app.auth.auth_access_token as auth_access_token
from app.auth.auth_who_am_i import get_user_from_jwt_data
from app.auth.utils import add_token_to_revoke_list


def refresh_access_token(Authorize: AuthJWT, db: Session) -> AccessToken:
    user_jwt = get_user_from_jwt_data(db, Authorize)
    jti = Authorize.get_raw_jwt()['jti']
    add_token_to_revoke_list(jti)
    new_access_token = auth_access_token.create_access_token(Authorize, user_jwt)
    return new_access_token


def get_refresh_token(Authorize: AuthJWT, db: Session, user: UserPassword) \
        -> RefreshToken:
    try:
        user_db = get_user(db, user)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    return create_refresh_token(Authorize, user_db)


def create_refresh_token(Authorize: AuthJWT, user_db: UserFullData) \
        -> RefreshToken:

    another_claims = {"user": user_db.username}
    refresh_token = Authorize.create_refresh_token(subject=user_db.id, user_claims=another_claims)
    return RefreshToken(refresh_token=refresh_token)
