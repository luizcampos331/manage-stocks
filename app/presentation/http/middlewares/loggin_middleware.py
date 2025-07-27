import time
import traceback
import uuid

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.infra.exceptions.infra_exception import InfraException
from app.infra.services.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    def handle_status_code(self, status: str) -> int:
        if status == "NOT_FOUND":
            return 404
        else:
            return 400

    async def dispatch(self, request: Request, call_next):
        incoming_request_id = request.headers.get("X-Request-ID")
        request_id = incoming_request_id or str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        try:
            response: Response = await call_next(request)
        except InfraException as e:
            logger.error(
                {
                    "request_id": request_id,
                    "error": f"{e.status}: {e.message}",
                    "trace": traceback.format_exc(),
                    "method": request.method,
                    "url": str(request.url),
                }
            )
            return JSONResponse(
                status_code=self.handle_status_code(e.status),
                content={
                    "status": e.status,
                    "message": e.message,
                    "request_id": request_id,
                },
            )
        except Exception as e:
            logger.error(
                {
                    "request_id": request_id,
                    "error": str(e),
                    "trace": traceback.format_exc(),
                    "method": request.method,
                    "url": str(request.url),
                }
            )
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "request_id": request_id},
            )

        process_time = time.time() - start_time

        if response.status_code < 400:
            logger.info(
                {
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "duration": f"{process_time:.3f}s",
                }
            )

        response.headers["X-Request-ID"] = request_id
        return response
