from sqlalchemy.orm import Session
from uuid import UUID
from app.models import user_models


def update_game_status(uuid: UUID, db: Session, status: str = 'done'):
    db.query().filter(user_models.Game.uuid == uuid)\
        .update({'status': status})
    db.commit()
