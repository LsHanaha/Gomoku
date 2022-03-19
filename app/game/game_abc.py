import abc
from sqlalchemy.orm import Session
from aioredis import Redis
from app.schemas import game_schemas

_COUNT_OF_HELPS = 3


class _GameABC(abc.ABC):
    def __init__(self, rule, uuid, dice_colors, field_type):
        self.field = self.__init_field()
        self.field_size = 19
        self.curr_player = 1
        self.count_of_turns = 0
        self.rule_name = rule
        self.uuid = uuid
        self.dice_colors = dice_colors
        self.field_type = field_type
        self.has_winner = False
        self.to_response = None
        self.score = [0, 0]  # имеет отношение только к конкретному правилу
        self.robot_help = {1: _COUNT_OF_HELPS, 2: _COUNT_OF_HELPS}

    @abc.abstractmethod
    async def change_player(self):
        pass

    @abc.abstractmethod
    async def set_move(self, move: game_schemas.Point):
        pass

    @abc.abstractmethod
    async def check_end_of_game(self, move: game_schemas.Point):
        pass

    @abc.abstractmethod
    async def perform_end_of_game(self, db: Session, redis: Redis):
        pass

    @abc.abstractmethod
    async def make_response(self):
        pass

    @abc.abstractmethod
    async def check_rule(self, move: game_schemas.Point, after_move=False):
        pass

    @staticmethod
    def __init_field():
        deck = []
        for i in range(19):
            deck.append([0] * 19)
        return deck


class HotSeatGameABC(_GameABC, abc.ABC):
    def __init__(self, rule, uuid, dice_colors, field_type):
        super().__init__(rule, uuid, dice_colors, field_type)


class RobotGameABC(_GameABC):

    def __init__(self, algorithm, algorithm_depth, is_debug, *args):

        self.algorithm_name = algorithm
        self.algorithm_depth = algorithm_depth
        self._last_robot_time = 0
        self.is_debug = is_debug
        super().__init__(*args)

    @abc.abstractmethod
    async def run_algorithm(self):
        pass

