from sqlalchemy.orm import Session

from app.models import user_models
from app.schemas import game_schemas


def init_game(data: dict, db: Session) -> game_schemas.Game:
    new_game = user_models.Game(
        user_id=data.get('user_id'),
        is_hot_seat=data['is_hot_seat'],
        status=data['status']
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


def store_settings(data: dict, db: Session) -> game_schemas.GameSettings:
    game_settings = user_models.GameSettings(
        game_id=data['game_id'],
        difficulty_id=data['difficulty'],
        rule_id=data['rule'],
        algorithm_id=data['algorithm'],
        is_debug=data['is_debug'],
        field_map=data['field'],
        dice_colors=data['dices']
    )

    db.add(game_settings)
    db.commit()
    db.refresh(game_settings)
    return game_settings


def add_game_in_history(data: dict, db: Session):
    stored_game = user_models.History(
        game_id=data['game_id'],
        winner=data['winner'],
        result=data['score'],
        move_count=data['count_of_turns']
    )
    db.add(stored_game)
    db.commit()
    db.refresh(stored_game)
    return stored_game
