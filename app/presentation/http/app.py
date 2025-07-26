from fastapi import FastAPI

from app.presentation.http.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Manage Stocks API",
        description="API for querying and registering stocks",
        version="0.1.0",
        contact={"name": "Luiz Campos", "email": "luizcampos331@gmail.com"},
        license_info={"name": "MIT"},
    )

    app.include_router(router)

    return app
