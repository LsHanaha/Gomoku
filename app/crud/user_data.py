from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from re import match
from datetime import datetime

from app.schemas import user_schema
from app.models import user_models


def get_user(db: Session, user: user_schema.UserPassword):
    if not match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9._%+-]+$",
                 user.username):
        res = get_user_by_username(db, user.username)
    else:
        res = get_user_by_email(db, user.username)

    if res is None:
        raise NoResultFound("Nothing found")

    return user_schema.UserFullData(id=res.id,
                                    username=res.username,
                                    email=res.email,
                                    password=res.password,
                                    validated=res.validated,
                                    validate_time=res.validate_time,
                                    active=res.active,
                                    creation_time=res.creation_time)


def get_user_by_username(db: Session, username: str) -> user_models.User:
    res = db.query(user_models.User).filter(user_models.User.username == username)\
        .first()
    return res


def get_user_by_email(db: Session, email: str) -> user_models.User:
    return db.query(user_models.User).filter(user_models.User.email == email) \
        .first()


def add_user(db: Session, user: user_schema.UserSignUp) -> user_schema.User:
    new_user = user_models.User(username=user.username,
                                email=user.email,
                                password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int) -> user_schema.UserFullData:

    res = db.query(user_models.User).filter(user_models.User.id == user_id).first()
    return user_schema.UserFullData(id=res.id,
                                    username=res.username,
                                    email=res.email,
                                    password=res.password,
                                    validated=res.validated,
                                    validate_time=res.validate_time,
                                    active=res.active,
                                    creation_time=res.creation_time)


def verify_user(db: Session, username: str) -> None:
    db_user: user_models.User = db.query(user_models.User).filter(user_models.User.username == username).first()
    db_user.validated = True
    db_user.validate_time = datetime.now()
    db_user.active = True
    db.commit()
    return


def update_password(db: Session, new_password: str, user: user_models.User) -> bool:
    user.password = new_password
    db.commit()
    return True
