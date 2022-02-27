import functools

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from app import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from sqlalchemy.orm import Session

from app import sync_redis
from app.schemas.user_schema import UserPassword, LoginToken, AccessToken, User, \
    UserSignUp, VerifyTokens, RestorePwdEmail, NewPassword
from app.auth.auth_access_token import get_tokens, refresh_access_token
from app.auth.auth_who_am_i import get_user_from_jwt_data
from app.auth import auth_signup, get_password_hash
from app.auth import auth_handle_mail
from app.crud import user_data as user_db

from app.models import get_db
from app.auth.utils import add_token_to_revoke_list


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)


def change_code_from_422_to_401(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            kwargs.get('authorize').jwt_required()
        except JWTDecodeError as err:
            status_code = err.status_code
            if err.message in ["Signature verification failed", 'Signature has expired']:
                status_code = 401
            raise HTTPException(status_code=status_code, detail=err.message)
        return func(*args, **kwargs)
    return wrapper


@router.post('/signin', response_model=LoginToken)
async def login(user: UserPassword, authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db)):
    res = get_tokens(user, authorize, db)
    return res


@router.post('/signup')
async def signup(user: UserSignUp, background_tasks: BackgroundTasks,
                 db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    auth_signup.add_new_user(user, db)
    background_tasks.add_task(auth_handle_mail.send_mail, user, authorize)
    return JSONResponse(status_code=201, content={"message": "User created. "
                                                             "Verification email sent."})


@router.get('/me', response_model=User)
@change_code_from_422_to_401
def who_am_i(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    user = get_user_from_jwt_data(db, authorize)
    return user


@router.post('/email-verification')
async def verify_email(token: VerifyTokens, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required("websocket", token=token.token)
    user = authorize.get_raw_jwt(token.token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    username = user.get('sub')
    if username is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_db.verify_user(db, username)
    add_token_to_revoke_list(user['jti'])
    return JSONResponse(status_code=201, content={"message": 'Email validated. Move to the login screen'})


@router.post('/restore-password', description="Sent email to restore password")
async def restore_password(email: RestorePwdEmail, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                     authorize: AuthJWT = Depends()):
    user = user_db.get_user_by_email(db, email.email)
    if not user:
        raise HTTPException(status_code=404, detail=f"Email {email.email} not found.")
    background_tasks.add_task(auth_handle_mail.send_password_restore_mail, user, authorize)
    return JSONResponse(status_code=201, content={"message": "Restore email sent."})


@router.get('/restore-password', description="Get token from user's email and validate his right to write new password")
async def parse_and_validate_restore_token(token: str, authorize: AuthJWT = Depends()):
    authorize.jwt_required("websocket", token=token)
    user = authorize.get_raw_jwt(token)
    if user.get('subject') != 'restore':
        raise HTTPException(status_code=403, detail="Token not allowed to restore password.")
    new_token = auth_handle_mail.create_add_passwd_token(authorize, user.get('sub'))
    add_token_to_revoke_list(user['jti'])
    return JSONResponse(status_code=200, content={'message': 'You can restore the password now',
                                                  'restore-token': new_token})


@router.post('/new-password')
async def save_new_password(data: NewPassword, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    authorize.jwt_required("websocket", token=data.token)
    jwt_user = authorize.get_raw_jwt(data.token)

    if jwt_user.get('subject') != 'new-passwd':
        raise HTTPException(status_code=403, detail="Token not allowed to restore password.")
    username = jwt_user.get('sub')
    user = user_db.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {username} not exists")

    new_password = get_password_hash(data.password)
    jti = jwt_user['jti']
    add_token_to_revoke_list(jti)

    mail_token = authorize.get_raw_jwt(data.restore_mail_token)
    mail_jti = mail_token['jti']
    add_token_to_revoke_list(mail_jti)

    if user_db.update_password(db, new_password, user):
        return JSONResponse(status_code=201, content={'message': 'Password updated. You can login now!'})
    return HTTPException(status_code=500, detail="OOOPs")


@router.post('/refresh', response_model=AccessToken)
async def refresh(authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()

    new_access_token = refresh_access_token(authorize, db, current_user)
    return new_access_token


# Endpoint for revoking the current users access token
@router.delete('/access-revoke')
async def access_revoke(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    # Store the tokens in redis with the value true for revoked.
    # We can also set an expires time on these tokens in redis,
    # so they will get automatically removed after they expired.
    jti = authorize.get_raw_jwt()['jti']
    sync_redis.hset("token", jti, 'true')
    return {"detail": " Access token has been revoke"}


# Endpoint for revoking the current users refresh token
@router.delete('/refresh-revoke')
async def refresh_revoke(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    jti = authorize.get_raw_jwt()['jti']
    sync_redis.hset("token", jti, 'true')
    return {"detail": "Refresh token has been revoke"}
