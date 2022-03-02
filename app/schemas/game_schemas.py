from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class Game(BaseModel):

    id: int
    user_id: Optional[int]
    uuid: UUID
    is_hot_seat: bool
    status: str

    class Config:
        orm_mode = True


class StoredGames(BaseModel):

    id: int
    game_id: int
    game_field: str
    score: str
    move_count: int

    class Config:
        orm_mode = True


class GameSettings(BaseModel):
    id: int
    game_id: int
    difficulty_id: Optional[int]
    rule_id: Optional[int]
    algorithm_id: Optional[int]
    is_debug: bool
    field_map: str
    dice_colors: str

    class Config:
        orm_mode = True


class DifficultyLevel(BaseModel):
    id: int
    name: str
    algorithm_depth: int

    class Config:
        orm_mode = True


class Algorithm(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Rule(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class NewGame(BaseModel):
    difficulties: List[DifficultyLevel]
    algorithms: List[Algorithm]
    rules: List[Rule]


class NewGamePostRequest(BaseModel):
    field: str
    dices: List[str]
    hot_seat: bool
    difficulty: int
    algorithm: int
    rule: int
    is_debug: bool


class NewGamePostResponse(BaseModel):
    uuid: UUID


class Point(BaseModel):
    row: int
    col: int
