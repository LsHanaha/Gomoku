import abc
from abc import ABC


class _GameABC(abc.ABC):
    def __init__(self, init_field, rule, uuid, dice_colors, field_type):
        self.field = init_field
        self.currPlayer = 1
        self.rule = rule
        self.uuid = uuid
        self.dice_colors = dice_colors
        self.field_type = field_type
        self.count_of_turns = 0

    @abc.abstractmethod
    async def init_spec_methods(self):
        pass

    @abc.abstractmethod
    async def change_player(self):
        pass

    @abc.abstractmethod
    async def set_move(self):
        pass

    @abc.abstractmethod
    async def check_end_of_game(self):
        pass

    @abc.abstractmethod
    async def make_response(self):
        pass


class HotSeatGameABC(_GameABC, ABC):
    def __init__(self, init_field, rule, uuid, dice_colors, field_type):
        super().__init__(init_field, rule, uuid, dice_colors, field_type)


class RobotGameABC(_GameABC):

    def __init__(self, algorithm, algorithm_depth, is_debug, *args):

        self.algorithm = algorithm
        self.algorithm_depth = algorithm_depth
        self._last_robot_time = 0
        self._is_debug = is_debug
        super().__init__(*args)

    @abc.abstractmethod
    async def run_algorythm(self):
        pass

    @abc.abstractmethod
    async def check_rule(self):
        pass

    @abc.abstractmethod
    async def rule(self):
        pass
