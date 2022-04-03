from aioredis import Redis
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Tuple, Optional, Union, Dict

from app.schemas import game_schemas
from app.crud.game import get_queries
from app.game import game_redis

from app.game import algorithms, rules, game_interfaces


class _CommonMethods:

    @staticmethod
    async def _set_rule(instance: Union[game_interfaces.HotSeatGame, game_interfaces.RobotGame]) -> None:
        rule_name = instance.rule_name
        rule_method = rules.rules.get(rule_name)
        if rule_method is None:
            raise KeyError(f"Rule {rule_name} not identified. Call developers")
        instance.check_rule = rule_method
        return


class NewGame:
    def __init__(self, db: Session, redis: Redis):
        self._db = db
        self._redis = redis

    async def create(self, data: game_schemas.NewGamePostResponse) -> bool:
        game_data = await self.get_game_by_uuid(data.uuid)
        if game_data.is_hot_seat:
            instance = await NewGameHotSeat(self._db).create(game_data)
        else:
            instance = await NewGameRobot(self._db).create(game_data)
        await self.store_instance_in_redis(instance)
        return True

    async def get_game_by_uuid(self, uuid: UUID) -> game_schemas.Game:
        game = get_queries.get_game_by_uuid(uuid, self._db)
        return game

    async def store_instance_in_redis(self, instance: Union[game_interfaces.HotSeatGame,
                                                            game_interfaces.RobotGame]) \
            -> None:
        await game_redis.store_in_redis(instance, self._redis)
        return


class NewGameHotSeat(_CommonMethods):

    def __init__(self, db: Session):
        self._db = db
        self._game_instance = game_interfaces.HotSeatGame

    async def create(self, game_data: game_schemas.Game):
        db_data = await self._get_db_data(game_data)
        game_instance = await self._initialize_game_instance(game_data, *db_data)
        return game_instance

    async def _get_db_data(self, game_data: game_schemas.Game) \
            -> Tuple[game_schemas.GameSettings, game_schemas.Rule]:
        settings = get_queries.get_game_settings(game_data.id, self._db)
        rule = get_queries.get_rule(settings.rule_id, self._db)
        return settings, rule

    async def _initialize_game_instance(self,
                                        game_data: game_schemas.Game,
                                        settings: game_schemas.GameSettings,
                                        rule: game_schemas.Rule) \
            -> game_interfaces.HotSeatGame:
        inst = self._game_instance(rule=rule.name, uuid=game_data.uuid, dice_colors=settings.dice_colors,
                                   field_type=settings.field_map)
        await self._set_rule(inst)
        await self._initialize_rule_status_code(inst)
        return inst

    @staticmethod
    async def _initialize_rule_status_code(inst: game_interfaces.HotSeatGame):
        await inst.generate_rule_status_code()


class NewGameRobot(_CommonMethods):

    def __init__(self, db: Session):
        self._db = db
        self._game_instance = game_interfaces.RobotGame

    async def create(self, game_data: game_schemas.Game):
        db_data = await self._get_db_data(game_data)
        game_instance = await self._initialize_game_instance(game_data, *db_data)
        return game_instance

    async def _get_db_data(self, game_data: game_schemas.Game) \
            -> Tuple[game_schemas.GameSettings, game_schemas.Rule,
                     game_schemas.DifficultyLevel, game_schemas.Algorithm]:
        settings = get_queries.get_game_settings(game_data.id, self._db)
        rule = get_queries.get_rule(settings.rule_id, self._db)
        difficulty = get_queries.get_difficulty(settings.difficulty_id, self._db)
        algorithm = get_queries.get_algorithm(settings.algorithm_id, self._db)
        return settings, rule, difficulty, algorithm

    async def _initialize_game_instance(self,
                                        game_data: game_schemas.Game,
                                        settings: game_schemas.GameSettings,
                                        rule: game_schemas.Rule,
                                        difficulty: game_schemas.DifficultyLevel,
                                        algorithm: game_schemas.Algorithm) \
            -> game_interfaces.RobotGame:

        inst = self._game_instance(rule=rule.name,
                                   uuid=game_data.uuid,
                                   dice_colors=settings.dice_colors,
                                   field_type=settings.field_map,
                                   algorithm=algorithm.name,
                                   algorithm_depth=difficulty.algorithm_depth,
                                   is_debug=settings.is_debug)
        await self._set_rule(inst)
        await self._set_algorithm(inst)
        await self._initialize_rule_status_code(inst)
        return inst

    @staticmethod
    async def _set_algorithm(instance: game_interfaces.RobotGame):
        algo_name = instance.algorithm_name
        algo_method = algorithms.algorithms.get(algo_name)
        if algo_method is None:
            raise KeyError(f"Rule {algo_name} not identified. Call developers")
        instance.run_algorithm = algo_method

    @staticmethod
    async def _initialize_rule_status_code(inst: game_interfaces.RobotGame):
        await inst.generate_rule_status_code()


class OldGame:

    def __init__(self, db: Optional[Session], redis: Redis):
        self._db = db
        self._redis = redis

    async def get_uuid(self, user_id: int) -> Dict[str, Optional[UUID]]:
        game: game_schemas.Game = await self._last_user_game_by_user_id(user_id)

        game_uuid = None
        if game:
            game_inst = await self.game_from_redis(game.uuid)
            if game_inst:
                game_uuid = game_inst.uuid
        return {"uuid": game_uuid}

    async def _last_user_game_by_user_id(self, user_id: int) \
            -> Optional[game_schemas.Game]:
        game = get_queries.get_last_game_for_user(user_id, self._db)
        if not game:
            return None

        if game.status == 'done':
            game = None
        return game

    async def game_from_redis(self, game_uuid: UUID) \
            -> Optional[Union[game_interfaces.HotSeatGame, game_interfaces.RobotGame]]:
        obj = await game_redis.load_from_redis(game_uuid, self._redis)
        if obj and not obj.has_winner:
            return obj
        return None
