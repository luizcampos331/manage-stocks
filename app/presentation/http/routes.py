from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.infra.factories.database.databse_config_factory import DatabaseConfigFactory
from app.infra.factories.queries.query_factory import QueryFactory
from app.infra.factories.services.cache_factory import CacheFactory
from app.infra.services.logger import logger
from app.presentation.http.controllers.stock_controller import stock_router

router = APIRouter()

router.include_router(stock_router)


def get_request_id(request: Request) -> str:
    return request.state.request_id


@router.get("/health", response_class=JSONResponse)
async def health(request: Request):
    request_id = request.state.request_id
    http_status = status.HTTP_200_OK
    health_report = {
        "cache": "ok",
        "database": "ok",
    }

    try:
        cache = CacheFactory().make()
        await cache.ping()
    except Exception as e:
        health_report["cache"] = "unavailable"
        logger.warning(
            {
                "request_id": request_id,
                "error": str(e),
                "message": "Health check: cache is not responding (ping failed).",
                "path": str(request.url),
            }
        )

    try:
        session = DatabaseConfigFactory().get_session()
        query_factory = QueryFactory().make(session)
        async with session:
            await query_factory.ping()
    except Exception as e:
        health_report["database"] = "unavailable"
        logger.error(
            {
                "request_id": request_id,
                "message": "Health check: database is not responding.",
                "error": str(e),
                "path": str(request.url),
            }
        )
        http_status = status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=http_status,
        content={
            "status": "ok" if http_status == 200 else "degraded",
            "details": health_report,
            "request_id": request_id,
        },
    )


@router.get("/", response_class=JSONResponse)
def root():
    return "Manage Stocks API 0.1.0"
