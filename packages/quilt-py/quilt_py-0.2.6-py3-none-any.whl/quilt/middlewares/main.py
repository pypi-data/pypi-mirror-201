import typing as T
import time
from fastapi import Request, Response, FastAPI
from quilt import logs

logger = logs.create_logger(__name__, one_color=logs.Color.PURPLE)

PROCESS_TIME_HEADER_NAME = "X-Process-Time-Ms"


def add_error_handling_and_process_time(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_error_handling_and_process_time_header(
        request: Request, call_next: T.Any
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers[PROCESS_TIME_HEADER_NAME] = str(process_time * 1_000)
        logger.debug("\n***Request Done***\n")
        return response
