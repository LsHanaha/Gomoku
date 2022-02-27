from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from typing import Union

from app.schemas.user_schema import UserSignUp, User
from app.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_address,
    MAIL_PASSWORD=settings.mail_pwd,
    MAIL_FROM=settings.mail_address,
    MAIL_FROM_NAME=settings.mail_user,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


async def send_mail(user: UserSignUp, authorize: AuthJWT):
    token = create_mail_token(authorize, user)

    message = MessageSchema(
        subject="Verify your e-mail address",
        recipients=[f"{user.email}"],
        body=f"""
                <div style="align-content: center;background-color: beige;width: 100%;height: auto">
                    <div style="text-transform: capitalize;font-size: 16px;font-weight: 600">
                        Click the followed link to activate your account:
                    </div>
                    <div>http://0.0.0.0:3000/email-verification/?token={token}</div>
                    <div>Your 42 comrads team</div>
                </div>
        """,
        subtype="html"
    )
    fm = FastMail(config=conf)
    await fm.send_message(message)


def create_mail_token(Authorize: AuthJWT, new_user: Union[UserSignUp, User]) \
        -> str:

    access_token = Authorize.create_access_token(subject=new_user.username,
                                                 expires_time=timedelta(seconds=settings.mail_token_lifetime))
    return access_token


async def send_password_restore_mail(user: User, authorize: AuthJWT):
    token = create_restore_token(authorize, user)

    message = MessageSchema(
        subject="Restore your password",
        recipients=[f"{user.email}"],
        body=f"""
                <div style="align-content: center;background-color: beige;width: 100%;height: auto">
                    <div style="text-transform: capitalize;font-size: 16px;font-weight: 600">
                        Click the followed link to restore your password.
                        If you not asked for this, just ignore this message.
                    </div>
                     <div> http://0.0.0.0:3000/restore-password/?token={token} </div>
                    <div>Your 42 comrads team</div>
                </div>
        """,
        subtype="html"
    )
    fm = FastMail(config=conf)
    await fm.send_message(message)


def create_restore_token(Authorize: AuthJWT, user: Union[UserSignUp, User]) \
        -> str:

    another_claims = {"subject": "restore"}
    access_token = Authorize.create_access_token(subject=user.username, user_claims=another_claims,
                                                 expires_time=timedelta(seconds=settings.mail_token_lifetime))
    return access_token


def create_add_passwd_token(Authorize: AuthJWT, username: str) \
        -> str:

    another_claims = {"subject": "new-passwd"}
    access_token = Authorize.create_access_token(subject=username, user_claims=another_claims,
                                                 expires_time=timedelta(seconds=settings.mail_token_lifetime))
    return access_token
