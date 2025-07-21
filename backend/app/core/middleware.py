import time
import logging
from typing import Callable
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Log request
        logger.info(
            f'Request: {request.method} {request.url.path} '
            f'Client: {request.client.host if request.client else "unknown"}'
        )

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(f'Response: {response.status_code} Process Time: {process_time:.4f}s Path: {request.url.path}')

        # Add processing time to response headers
        response.headers['X-Process-Time'] = str(process_time)

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            # Log the HTTPException (including ValidationError)
            logger.error(f'HTTPException in {request.method} {request.url.path}: {http_exc.detail}')
            return Response(
                content=f'{{"detail": "{http_exc.detail}"}}',
                status_code=http_exc.status_code,
                media_type='application/json',
            )
        except Exception as e:
            logger.error(f'Unhandled error in {request.method} {request.url.path}: {str(e)}')
            raise
