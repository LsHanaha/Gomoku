"""
Some rules can check end of game condition. Some rules have to check end of game
condition. This games
"""

from typing import Optional
from app.game import game_abc
from app.schemas import game_schemas
from app.errors import GomokuError
from app.game.game_helpers import check_end_of_game


async def _no_rules(*args, **kwargs) -> None:
    return


async def _choice_of_redaction():
    pass


async def _karo(game: game_abc._GameABC, move: game_schemas.Point, after_move: bool) \
        -> Optional[bool]:
    if not after_move:
        return
    sequences = await check_end_of_game(game, move)
    status = any(stones >= 5 for stones, is_surrounded in sequences.lengths
                 if not is_surrounded)
    game.has_winner = status
    return status


async def _forbidden_square(game: game_abc._GameABC, move: game_schemas.Point, after_move: bool) \
        -> None:
    if after_move:
        return
    if game.count_of_turns == 2:
        if 7 <= move.row <= 11 and 7 <= move.col <= 11:
            raise GomokuError("Move not available for forbidden saqure rule! "
                              "Turn should be out of central square 5x5!")


async def _common_center(game: game_abc._GameABC, move: game_schemas.Point, after_move: bool) \
        -> None:
    if after_move:
        return
    if game.count_of_turns > 2:
        return
    if move.row == move.col == 9:
        raise GomokuError("Move not available for common center rule!")
    # Place a center stone for the second user
    if game.count_of_turns == 1:
        game.field[9][9] = 2


rules = {
    'no rules': _no_rules,
    'Choice of redaction': _choice_of_redaction,
    'Karo': _karo,
    'Forbidden square': _forbidden_square,
    'Common center': _common_center
}
