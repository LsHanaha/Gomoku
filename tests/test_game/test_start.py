import json

import pytest

from datetime import timedelta
from app.config import settings
from app.schemas.game_schemas import NewGamePostRequest


@pytest.mark.asyncio
async def test_stored_game(app_with_game_tables, authorization_fixture):
    token = authorization_fixture.create_access_token(
        subject="test_user",
        expires_time=timedelta(seconds=settings.mail_token_lifetime)
    )
    response = await app_with_game_tables.get("/game/check-stored", headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_stored_game_unauthorized(app_with_game_tables):

    response = await app_with_game_tables.get("/game/check-stored")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_new_game_data(app_with_game_tables):

    data = await app_with_game_tables.get('/game/new-game')
    assert data.status_code == 200
    data = data.json()
    assert set(data.keys()) == {'difficulties', 'rules', 'algorithms'}


@pytest.mark.asyncio
@pytest.mark.parametrize('request_data',
             [
                 NewGamePostRequest(field='default', dices=['black', 'white'],
                                    hot_seat=False, difficulty=1, algorithm=1, rule=1,
                                    is_debug=False),
                 NewGamePostRequest(field='default', dices=['black', 'white'],
                                    hot_seat=True, difficulty=1, algorithm=1, rule=1,
                                    is_debug=True)
             ]
)
async def test_create_new_game(app_with_game_tables, authorization_fixture, create_user, request_data):

    token = authorization_fixture.create_access_token(
        subject="1",
        expires_time=timedelta(seconds=settings.mail_token_lifetime)
    )

    data = await app_with_game_tables.post('/game/new-game', content=json.dumps(request_data.dict()),
                                           headers={'Authorization': f"Bearer {token}"})
    assert data.status_code == 201
    assert data.json().get('uuid') is not None


@pytest.mark.asyncio
@pytest.mark.parametrize('request_data',
             [
                 NewGamePostRequest(field='default', dices=['black', 'white'],
                                    hot_seat=False, difficulty=1, algorithm=1, rule=1,
                                    is_debug=False),
                 NewGamePostRequest(field='default', dices=['black', 'white'],
                                    hot_seat=True, difficulty=1, algorithm=1, rule=1,
                                    is_debug=True)
             ]
)
async def test_create_new_game_unauthorized(app_with_game_tables, request_data):

    data = await app_with_game_tables.post('/game/new-game', content=json.dumps(request_data.dict()))
    assert data.status_code == 201
    assert data.json().get('uuid') is not None
