from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List
from uuid import UUID

from app.models import user_models
from app.schemas import game_schemas


def get_difficulties(db: Session) -> List[game_schemas.DifficultyLevel]:
    difficulties = db.query(user_models.DifficultyLevel).all()
    return difficulties


def get_algorithms(db: Session) -> List[game_schemas.Algorithm]:
    data = db.query(user_models.GomokuAlgorithm).all()
    return data


def get_rules(db: Session) -> List[game_schemas.Rule]:
    data = db.query(user_models.Rule).all()
    return data


def get_game_by_uuid(uuid: UUID, db: Session) -> game_schemas.Game:
    data = db.query(user_models.Game).where(user_models.Game.uuid == uuid).first()
    return data


def get_last_game_for_user(user_id: int, db: Session) -> game_schemas.Game:
    data = db.query(user_models.Game).where(user_models.Game.user_id == user_id)\
        .order_by(desc(user_models.Game.created_at)).first()
    return data


def get_game_settings(game_id: int, db: Session):
    data = db.query(user_models.GameSettings).where(user_models.GameSettings.game_id == game_id).first()
    return data


def get_algorithm(algorithm_id: int, db: Session) -> game_schemas.Algorithm:
    db_data = db.query(user_models.GomokuAlgorithm)\
        .where(user_models.GomokuAlgorithm.id == algorithm_id)\
        .first()
    data = game_schemas.Algorithm(id=db_data.id, name=db_data.name)
    return data


def get_difficulty(difficulty_id: int, db: Session) -> game_schemas.DifficultyLevel:
    db_data = db.query(user_models.DifficultyLevel)\
        .where(user_models.DifficultyLevel.id == difficulty_id)\
        .first()
    data = game_schemas.DifficultyLevel(id=db_data.id, name=db_data.name, algorithm_depth=db_data.algorithm_depth)
    return data


def get_rule(rule_id: int, db: Session) -> game_schemas.Rule:
    db_data = db.query(user_models.Rule)\
        .where(user_models.Rule.id == rule_id)\
        .first()
    data = game_schemas.Rule(id=db_data.id, name=db_data.name)
    return data
