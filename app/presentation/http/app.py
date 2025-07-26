from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.presentation.http.handlers.http_exception_handler import http_exception_handler
from app.presentation.http.handlers.validation_exception_handler import (
    validation_exception_handler,
)
from app.presentation.http.middlewares.loggin_middleware import LoggingMiddleware
from app.presentation.http.routes import router

ALLOW_ORIGINS = ["*"]


def create_app() -> FastAPI:
    app = FastAPI(
        title="Manage Stocks API",
        description="API for querying and registering stocks",
        version="0.1.0",
        contact={"name": "Luiz Campos", "email": "luizcampos331@gmail.com"},
        license_info={"name": "MIT"},
    )

    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.include_router(router)

    return app
