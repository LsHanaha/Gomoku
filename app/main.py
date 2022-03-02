import traceback
import logging
from typing import Optional, Type
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.models import engine
from app.models import user_models
from app.auth.endpoints import router as router_auth
from app.game.endpoints import game_router
from app.errors import GomokuError
from app import get_async_redis_conn

middleware = [Middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True,
                         allow_methods=['*'], allow_headers=['*'])]

# create tables if not exist
user_models.Base.metadata.create_all(bind=engine)


def create_app():

    app_ = FastAPI(middleware=middleware)

    # change logger
    app_.error_logger = logging.getLogger('uvicorn.error')
    app_.default_logger = logging.getLogger('uvicorn')

    # add application blueprints
    app_.include_router(game_router)
    app_.include_router(router_auth)

    return app_


web_app = create_app()


@web_app.on_event("startup")
async def create_redis():
    web_app.state.redis = await get_async_redis_conn()


@web_app.on_event("shutdown")
async def close_redis():
    await web_app.state.redis.close()


def get_app_middleware(app_: FastAPI, middleware_class: Type) -> Optional[Middleware]:
    middleware_index = None
    for index, middleware_ in enumerate(app_.user_middleware):
        if middleware_.cls == middleware_class:
            middleware_index = index
    return None if middleware_index is None else app_.user_middleware[middleware_index]


@web_app.exception_handler(AuthJWTException)
async def auth_jwt_exception_handler(request: Request, exc):
    trace = traceback.format_exc()
    request.app.error_logger.critical(
        f"Start error message\n"
        f"{request.url.path} {exc.status_code} JWT Token Error.\n{trace}\n"
        f"Error message complete"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@web_app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc):
    trace = traceback.format_exc()
    request.app.error_logger.critical(
        f"Start error message\n"
        f"{request.url.path} {status.HTTP_500_INTERNAL_SERVER_ERROR} Value Error.\n{trace}"
        f"Error message complete"
    )
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


@web_app.exception_handler(GomokuError)
async def expected_errors_handler(request: Request, exc):
    request.app.default_logger.info(
        f"An expected error occurred:\n {str(exc)}"
    )
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "is_error": True}
    )


@web_app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    trace = traceback.format_exc()
    request.app.error_logger.critical(
        f"Start error message\n"
        f"{request.url.path} {status.HTTP_500_INTERNAL_SERVER_ERROR} Internal Server Error.\n{trace}"
        f"Error message complete"
    )
    response = JSONResponse({'detail': f'Internal error "{str(exc) if str(exc) else "unresolved"}"'.upper()},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    cors_middleware = get_app_middleware(app_=request.app, middleware_class=CORSMiddleware)

    request_origin = request.headers.get("origin", "")

    if cors_middleware and "*" in cors_middleware.options["allow_origins"]:
        response.headers["Access-Control-Allow-Origin"] = "*"
    elif cors_middleware and request_origin in cors_middleware.options["allow_origins"]:
        response.headers["Access-Control-Allow-Origin"] = request_origin

    return response
