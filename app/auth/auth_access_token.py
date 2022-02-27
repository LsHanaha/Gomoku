from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import timedelta

from typing import Optional


from app.schemas.user_schema import UserPassword, LoginToken, RefreshToken, \
    AccessToken, UserFullData
from app.crud.user_data import get_user, get_user_by_id
import app.auth.auth_refresh_token as auth_refresh_token
from . import verify_password
from app.config import settings

_JWT_EXPIRATION = settings.token_lifetime_sec


def get_tokens(user: UserPassword, Authorize: AuthJWT, db: Session) -> Optional[LoginToken]:
    try:
        user_db = get_user(db, user)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")
    if not validate_user_credentials(user, user_db):
        raise HTTPException(status_code=404, detail="Username or password not valid")
    if not user_db.validated:
        raise HTTPException(status_code=403, detail="This account email was not verified. Check your mail box")
    if not user_db.active:
        raise HTTPException(status_code=403, detail="Данный аккаунт был забанен. По всем вопросам обращайтесь "
                                                    "к разработчикам")

    tokens = sign_tokens(Authorize, user_db)
    return tokens


# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
def validate_user_credentials(user: UserPassword, user_db: UserFullData) -> bool:
    if not (user.username == user_db.username or user.username == user_db.email) or \
            not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    return True


def sign_tokens(Authorize: AuthJWT, user_db: UserFullData) \
        -> LoginToken:

    access_token: AccessToken = create_access_token(Authorize, user_db)
    refresh_token: RefreshToken = auth_refresh_token.create_refresh_token(Authorize, user_db)

    return LoginToken(access_token=access_token.access_token,
                      refresh_token=refresh_token.refresh_token)


def create_access_token(Authorize: AuthJWT, user_db: UserFullData) \
        -> AccessToken:

    another_claims = {"user": user_db.username}
    access_token = Authorize.create_access_token(subject=user_db.id, user_claims=another_claims,
                                                 expires_time=timedelta(seconds=int(_JWT_EXPIRATION)))
    return AccessToken(access_token=access_token)


def refresh_access_token(Autorize: AuthJWT, db: Session, user_id) -> AccessToken:
    user_db: UserFullData = get_user_by_id(db, user_id)
    return create_access_token(Autorize, user_db)
