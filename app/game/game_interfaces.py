from app.game.game_abc import HotSeatGameABC, RobotGameABC


class HotSeatGame(HotSeatGameABC):

    def __init__(self, init_field, rule, uuid, dice_colors, field_type):
        super().__init__(init_field, rule, uuid, dice_colors, field_type)
        pass

    async def init_spec_methods(self):
        pass

    async def change_player(self):
        pass

    async def set_move(self):
        pass

    async def check_end_of_game(self):
        pass

    async def make_response(self):
        pass


class RobotGame(RobotGameABC):
    def __init__(self, algorithm, algorithm_depth, is_debug, init_field, rule, uuid, dice_colors, field_type):
        super().__init__(algorithm, algorithm_depth, is_debug, init_field, rule, uuid, dice_colors, field_type)

    async def init_spec_methods(self):
        pass

    async def change_player(self):
        pass

    async def set_move(self):
        pass

    async def check_end_of_game(self):
        pass

    async def make_response(self):
        pass

    async def run_algorythm(self):
        pass

    async def check_rule(self):
        pass

    async def rule(self):
        pass
