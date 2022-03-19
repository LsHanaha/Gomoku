import uuid

from sqlalchemy.orm import Session
from typing import Optional

from app.crud.game import get_queries, post_queries, update_queries
from app.schemas import game_schemas


class DataForNewGame:
    def __init__(self, db: Session):
        self._db = db

    async def collect_all(self) -> game_schemas.NewGame:
        difficulties = await self.difficulties()
        algorithms = await self.algorithms()
        rules = await self.rules()
        result = game_schemas.NewGame(
            algorithms=algorithms,
            rules=rules,
            difficulties=difficulties
        )
        return result

    async def difficulties(self):
        data = get_queries.get_difficulties(self._db)
        return data

    async def algorithms(self):
        data = get_queries.get_algorithms(self._db)
        return data

    async def rules(self):
        data = get_queries.get_rules(self._db)
        return data


class NewGameData:

    def __init__(self, db: Session):
        self._db = db

    async def store(self, data: game_schemas.NewGamePostRequest, user_id: Optional[int] = None) \
            -> game_schemas.NewGamePostResponse:
        new_game = await self._store_game_data(data, user_id)
        await self._add_settings(data, new_game)
        return game_schemas.NewGamePostResponse(uuid=new_game.uuid)

    async def _store_game_data(self, data: game_schemas.NewGamePostRequest, user_id: Optional[int] = None):
        await self._deactivate_old_games(user_id)
        new_game = await self._add_new_game(data, user_id)
        return new_game

    async def _deactivate_old_games(self, user_id: int):
        update_queries.update_games_statuses_for_user(user_id, self._db)
        return

    async def _add_new_game(self, data: game_schemas.NewGamePostRequest, user_id) \
            -> game_schemas.Game:
        game_data = {
            'user_id': user_id,
            'is_hot_seat': data.hot_seat,
            'status': 'active'
        }
        new_game = post_queries.init_game(game_data, self._db)
        return new_game

    async def _add_settings(self, data: game_schemas.NewGamePostRequest, game: game_schemas.Game) \
            -> game_schemas.GameSettings:
        settings_data = {
            'game_id': game.id,
            'field': data.field,
            'dices': ':'.join(data.dices),
            'difficulty': None,
            'rule': data.rule,
            'algorithm': None,
            'is_debug': False
        }
        if not data.hot_seat:
            settings_data['difficulty'] = data.difficulty
            settings_data['algorithm'] = data.algorithm
            settings_data['is_debug'] = data.is_debug

        game_settings = post_queries.store_settings(settings_data, self._db)
        return game_settings
