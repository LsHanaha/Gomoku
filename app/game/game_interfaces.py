from sqlalchemy.orm import Session
from app.game.game_abc import HotSeatGameABC, RobotGameABC
from app.schemas import game_schemas
from app.errors import GomokuError

from app.crud.game import update_queries, post_queries, get_queries


class HotSeatGame(HotSeatGameABC):
    """
    This src is a set of rules, which will be called in game arena
    """

    def __init__(self, rule, uuid, dice_colors, field_type):
        super().__init__(rule, uuid, dice_colors, field_type)

    async def change_player(self) -> None:
        self.curr_player = 1 if self.curr_player == 2 else 2

    async def set_move(self, point: game_schemas.Point):
        if self.field[point.row][point.col]:
            raise GomokuError(f"This point is not empty!")
        self.field[point.row][point.col] = self.curr_player

    async def check_end_of_game(self):
        pass

    async def perform_end_of_game(self, db: Session):
        game: game_schemas.Game = get_queries.get_game_by_uuid(self.uuid, db)
        if game.user_id:
            post_queries.add_game_in_history({
                'game_id': game.id,
                'winner': f"Player {self.curr_player}",
                'score': self.score[self.curr_player],
                'count_of_turns': self.count_of_turns
            }, db)
        update_queries.update_game_status(self.uuid, db)

    async def make_response(self):
        pass

    async def check_rule(self) -> bool:
        raise GomokuError(f"Can't set this move, forbidden by rule")

    @staticmethod
    async def run_algorithm():
        # dummy method to handle arenas methods consequence
        return None


class RobotGame(RobotGameABC):

    def __init__(self, rule, uuid, dice_colors, field_type, algorithm, algorithm_depth, is_debug):
        super().__init__(algorithm, algorithm_depth, is_debug, rule, uuid, dice_colors, field_type)

    async def change_player(self):
        self.curr_player = 1 if self.curr_player == 2 else 2

    async def set_move(self, point: game_schemas.Point):
        if self.field[point.row][point.col]:
            raise GomokuError(f"This point is not empty!")
        self.field[point.row][point.col] = self.curr_player

    async def check_end_of_game(self):
        pass

    async def perform_end_of_game(self, db: Session):
        game: game_schemas.Game = get_queries.get_game_by_uuid(self.uuid, db)
        if game.user_id:
            post_queries.add_game_in_history({
                'game_id': game.id,
                'winner': f"Player {self.curr_player}",
                'score': self.score[self.curr_player],
                'count_of_turns': self.count_of_turns
            }, db)
        update_queries.update_game_status(self.uuid, db)

    async def make_response(self):
        pass

    async def run_algorithm(self):
        pass

    async def check_rule(self):
        pass
