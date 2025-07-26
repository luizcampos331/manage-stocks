from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.infra.services.logger import logger


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    request_id = getattr(request.state, "request_id", None)
    logger.warning(
        {
            "request_id": request_id,
            "error": str(exc.detail),
            "status_code": exc.status_code,
            "path": str(request.url),
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "request_id": request_id},
    )
