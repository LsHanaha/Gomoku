from sqlalchemy import and_
from sqlalchemy.orm import Session
from uuid import UUID
from app.models import user_models


def update_game_status(uuid: UUID, db: Session, status: str = 'done'):
    db.query(user_models.Game).filter(user_models.Game.uuid == uuid)\
        .update({'status': status})
    db.commit()


def update_games_statuses_for_user(user_id: int, db: Session, status: str = 'done'):
    db.query(user_models.Game).filter(and_(user_models.Game.user_id == user_id, user_models.Game.status == 'active')) \
        .update({'status': status})
    db.commit()
