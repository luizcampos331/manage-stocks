from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.infra.services.logger import logger


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", None)

    logger.warning(
        {
            "request_id": request_id,
            "validation_errors": exc.errors(),
            "path": str(request.url),
        }
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "request_id": request_id,
        },
    )
