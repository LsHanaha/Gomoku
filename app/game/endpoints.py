from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from sqlalchemy.orm import Session
from typing import Optional, List

from app import AuthJWT
from app.models import get_db
from app.schemas import game_schemas

from app.game import parameters
from app.game import game as _create_game
from app.game.arena import Arena
from app.game import processing


game_router = APIRouter(
    prefix="/game",
    tags=['game'],
    responses={404: {"description": "Not found"}}
)


@game_router.get("/check-stored", response_model=game_schemas.NewGamePostResponse)
async def has_stored_game(request: Request, authorize: AuthJWT = Depends(),
                          db: Session = Depends(get_db)):
    # Проверяем есть ли незаконченная игра. Возвращаем uuid если да и None если нет
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    game_uuid = await _create_game.OldGame(db, request.app.state.redis).get_uuid(user_id)
    return game_uuid


@game_router.get("/new-game", response_model=game_schemas.NewGame)
async def new_game(db: Session = Depends(get_db)):
    # получение списка противников, сложностей, настроек игры, перечня правил
    data = await parameters.DataForNewGame(db).collect_all()
    return data


@game_router.post("/new-game", response_model=game_schemas.NewGamePostResponse, status_code=201)
async def new_game(data: game_schemas.NewGamePostRequest, authorize: AuthJWT = Depends(),
                   db: Session = Depends(get_db)) -> game_schemas.NewGamePostResponse:
    # Сохранение списка противников, сложностей, настроек игры, перечня правил и пр. Возвращает id игры
    authorize.jwt_optional()
    user_id = authorize.get_jwt_subject()
    if user_id:
        user_id = int(user_id)
    uuid = await parameters.NewGameData(db).store(data, user_id)
    return uuid


@game_router.post("/start")
async def start_game(request: Request, data: game_schemas.NewGamePostResponse,
                     db: Session = Depends(get_db)):
    # get id of game (new or existing). Init game and return status of operation
    redis = request.app.state.redis
    status = await _create_game.NewGame(db, redis).create(data)
    return JSONResponse({'status': status})


@game_router.post("/move", response_model=game_schemas.GameResponse)
async def user_move(request: Request, game_point: game_schemas.Point,
                    db: Session = Depends(get_db)):
    # get user move and game id, check rules and game status. Generates robot move.
    # return game status and robot move (if necessary). Возможна отбивка об ошибке в случае если
    # нарушается правило
    game = await _create_game.OldGame(None, request.app.state.redis).game_from_redis(game_point.uuid)
    result = await Arena(db, request.app.state.redis).run(game, game_point)
    return result


@game_router.post('/help', response_model=game_schemas.GameResponse)
async def lend_a_hand_from_robot(request: Request, game_uuid: game_schemas.NewGamePostResponse,
                                 db: Session = Depends(get_db)):
    # Робот поможет юзеру с ходом. Предположительно, количество будет ограничено.
    # Возвращает рекомендованный ход
    game = await _create_game.OldGame(None, request.app.state.redis).game_from_redis(game_uuid.uuid)
    result = await processing.robot_help(game, db, request.app.state.redis)
    return result


@game_router.post('/game-start', response_model=Optional[game_schemas.InitGameData])
async def get_start_data(request: Request, game: game_schemas.NewGamePostResponse):
    start_data = await processing.init_game_data(request.app.state.redis, game.uuid)
    return start_data


@game_router.get('/history', response_model=List[game_schemas.GameHistory])
async def get_user_history(db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    result = await processing.get_user_history(user_id, db)
    return result
