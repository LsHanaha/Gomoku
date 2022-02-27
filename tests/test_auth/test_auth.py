import pytest
import json

from datetime import timedelta
from app.auth import auth_handle_mail
from app.config import settings


@pytest.mark.asyncio
async def test_create_user(test_application, monkeypatch):
    request_payload = {"username": "test_user", "email": "kirik193@yandex.ru", "password": "password"}

    async def send_mail_override(*args, **kwargs):
        pass

    monkeypatch.setattr(auth_handle_mail, "send_mail", send_mail_override)

    response = await test_application.post("/auth/signup", content=json.dumps(request_payload))
    assert response.status_code == 201
    assert response.text == '{"message":"User created. Verification email sent."}'


@pytest.mark.asyncio
@pytest.mark.parametrize('payload, result', [({"username": "test_user", "password": "password"}, None),
                                             ({"username": "kirik193@yandex.ru", "password": "password"}, None)])
async def test_get_user_not_validated(test_application, payload, result):

    response = await test_application.post("/auth/signin", content=json.dumps(payload))

    assert response.status_code == 403
    assert response.text == '{"detail":"This account email was not verified. Check your mail box"}'


@pytest.mark.asyncio
async def test_validate(test_application, authorization_fixture):
    token = authorization_fixture.create_access_token(
        subject="test_user",
        expires_time=timedelta(seconds=settings.mail_token_lifetime)
    )
    assert isinstance(token, str)

    response = await test_application.post("/auth/email-verification", content=json.dumps({'token': token}))
    assert response.status_code == 201
    assert response.text == '{"message":"Email validated. Move to the login screen"}'


@pytest.mark.asyncio
@pytest.mark.parametrize('payload', [({"username": "test_user", "password": "password"}),
                                     ({"username": "kirik193@yandex.ru", "password": "password"})])
async def test_get_user_validated(test_application, payload):

    response = await test_application.post("/auth/signin", content=json.dumps(payload))

    assert response.status_code == 200
    assert list(response.json()) == ['refresh_token', 'access_token']


@pytest.mark.asyncio
@pytest.mark.parametrize('payload', [({"username": "test_user", "password": "password"}),
                                     ({"username": "kirik193@yandex.ru", "password": "password"})])
async def test_get_me(test_application, payload):

    response_auth = await test_application.post("/auth/signin", content=json.dumps(payload))

    assert response_auth.status_code == 200
    assert list(response_auth.json()) == ['refresh_token', 'access_token']

    access_token = response_auth.json()['access_token']

    response_me = await test_application.get('/auth/me', headers={'Authorization': f"Bearer {access_token}"})

    assert response_me.status_code == 200
    assert payload['username'] in [response_me.json()['email'], response_me.json()['username']]
