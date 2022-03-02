from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from sqlalchemy.orm import Session

from app import AuthJWT
from app.models import get_db
from app.schemas import game_schemas

from app.game import parameters
from app.game import game as _create_game

from app.game import game_in_redis


game_router = APIRouter(
    prefix="/game",
    tags=['game'],
    responses={404: {"description": "Not found"}}
)


@game_router.get("/check-stored")
async def has_stored_game(request: Request, authorize: AuthJWT = Depends(),
                          db: Session = Depends(get_db)):
    # Проверяем есть ли незаконченная игра. Возвращаем ответ да или нет
    authorize.jwt_required()
    user = authorize.get_jwt_subject()
    game = await _create_game.OldGame().last_user_game_by_user_id(user, db)

    status = False
    if game:
        obj = await game_in_redis.load_from_redis(game.uuid, request.app.state.redis)
        if obj and not obj.has_winner:
            status = True

    return JSONResponse({'is_stored_game': status})


@game_router.get("/new-game", response_model=game_schemas.NewGame)
async def new_game(db: Session = Depends(get_db)):
    # получение списка противников, сложностей, настроек игры, перечня правил
    data = await parameters.NewGameData(db).collect_all()
    return data


@game_router.post("/new-game", response_model=game_schemas.NewGamePostResponse, status_code=201)
async def new_game(data: game_schemas.NewGamePostRequest, authorize: AuthJWT = Depends(),
                   db: Session = Depends(get_db)) -> game_schemas.NewGamePostResponse:
    # Сохранение списка противников, сложностей, настроек игры, перечня правил и пр. Возвращает id игры
    authorize.jwt_optional()
    user_id = authorize.get_jwt_subject()
    if user_id:
        user_id = int(user_id)
    uuid = await parameters.NewGameSettings(db).store(data, user_id)
    return uuid


@game_router.post("/start")
async def start_game(request: Request, data: game_schemas.NewGamePostResponse,
                     db: Session = Depends(get_db), authorize: AuthJWT = Depends()):
    # get id of game (new or existing). Init game and return status of operation
    redis = request.app.state.redis
    status = await _create_game.NewGame(db, redis).create(data)
    return JSONResponse({'status': status})


@game_router.post("/move")
async def user_move():
    # get user move and game id, check rules and game status. Generates robot move.
    # return game status and robot move (if necessary). Возможна отбивка об ошибке в случае если
    # нарушается правило
    pass


@game_router.get('/help')
async def lend_a_hand_from_robot():
    # Робот поможет юзеру с ходом. Предположительно, количество будет ограничено.
    # Возвращает рекомендованный ход
    pass
