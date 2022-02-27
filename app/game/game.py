
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas import game_schemas
from app.crud.game import get_queries

from app.game import algorithms, rules


class NewGame:

    def __init__(self, db: Session):
        self._db = db

    async def create(self, data: game_schemas.NewGamePostResponse):
        game, settings, rule = await self._get_db_data(data.uuid)
        if not game.is_hot_seat:
            difficulty, algorithm = await self._get_additional_db_data(settings)



    async def _get_db_data(self, uuid: UUID):
        game = get_queries.get_game_by_uuid(uuid, self._db)
        settings = get_queries.get_game_settings(game.id, self._db)
        rule = get_queries.get_rule(settings.rule_id, self._db)
        return game, settings, rule

    async def _get_additional_db_data(self, settings):
        difficulty = get_queries.get_difficulty(settings.difficulty_id, self._db)
        algorithm = get_queries.get_algorithm(settings.algorithm_id, self._db)
        return difficulty, algorithm


class OldGame:

    async def load(self, uuid: UUID, db: Session):
        pass
