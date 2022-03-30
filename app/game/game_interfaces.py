from sqlalchemy.orm import Session
from aioredis import Redis
from uuid import UUID
from copy import copy
import algo_module
from app.game.game_abc import HotSeatGameABC, RobotGameABC
from app.schemas import game_schemas
from app.errors import GomokuError

from app.crud.game import update_queries, post_queries, get_queries
from app.game import game_redis
from app.game.game_helpers import check_end_of_game


ALLOW_CAPTURE = 0b00001
FREE_THREE = 0b00010
RESTRICTED_SQUARE = 0b00100
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
        self.count_of_turns += 1

    async def check_end_of_game(self, move: game_schemas.Point):
        sequences = await check_end_of_game(self, move)
        status = any(i >= 5 for i in sequences.lengths)
        if status:
            self.has_winner = True

    async def perform_end_of_game(self, db: Session, redis: Redis):
        game: game_schemas.Game = get_queries.get_game_by_uuid(self.uuid, db)
        if game.user_id:
            post_queries.add_game_in_history({
                'game_id': game.id,
                'winner': f"Player {self.curr_player}",
                'score': f"{self.score[0]} : {self.score[1]}",
                'count_of_turns': self.count_of_turns
            }, db)
        update_queries.update_game_status(self.uuid, db)
        await game_redis.delete_game(self, redis)

    async def make_response(self) -> game_schemas.GameContinue:
        response = game_schemas.GameContinue(
            map=self.field,
            debug=None,
            score=self.score,
            robot_time=None,
            count_of_turns=self.count_of_turns,
            current_player=self.curr_player
        )
        return response

    async def check_rule(self, move: game_schemas.Point, after_move=False) -> bool:
        pass

    @staticmethod
    async def run_algorithm():
        # dummy method to handle arena sequence
        return None


class RobotGame(RobotGameABC):

    def __init__(self, rule, uuid, dice_colors, field_type, algorithm, algorithm_depth, is_debug):
        super().__init__(algorithm, algorithm_depth, is_debug, rule, uuid, dice_colors, field_type)

    async def change_player(self):
        self.curr_player = 1 if self.curr_player == 2 else 2

    async def set_move(self, move: game_schemas.Point):
        if self.field[move.row][move.col]:
            raise GomokuError(f"This point is not empty!")
        rules = int(7)
        # if True:
        #     rules |= ALLOW_CAPTURE
        # if True:
        #     rules |= FREE_THREE
        # if True:
        #     rules |= RESTRICTED_SQUARE
        enemy = int(1 if self.curr_player == 2 else 2)
        is_capture = algo_module.implement_move(self.field, self.curr_player, enemy, rules, move.row, move.col)
        # if is_capture:
        #     Добавить баллы за захват
        self.count_of_turns += 1

    async def check_end_of_game(self, move: game_schemas.Point):
        sequences = await check_end_of_game(self, move)
        status = any(i >= 5 for i in sequences.lengths)
        if status:
            self.has_winner = True

    async def perform_end_of_game(self, db: Session, redis: Redis):
        game: game_schemas.Game = get_queries.get_game_by_uuid(self.uuid, db)
        if game.user_id:
            post_queries.add_game_in_history({
                'game_id': game.id,
                'winner': f"Player {self.curr_player}",
                'score': f"{self.score[0]} : {self.score[1]}",
                'count_of_turns': self.count_of_turns
            }, db)
        update_queries.update_game_status(self.uuid, db)
        await game_redis.delete_game(self, redis)

    async def make_response(self) -> game_schemas.GameContinue:
        response = game_schemas.GameContinue(
            map=self.field,
            debug=copy(self.debug_data),
            score=self.score,
            robot_time=copy(self.last_robot_time),
            count_of_turns=self.count_of_turns,
            current_player=self.curr_player
        )
        self.debug_data = None
        self.last_robot_time = None
        return response

    async def run_algorithm(self, game) -> game_schemas.Point:
        # TODO remove mock
        pass

    async def check_rule(self, move: game_schemas.Point, after_move=False):
        pass
