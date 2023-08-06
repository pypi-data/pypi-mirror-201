import typing as T
import time
from contextlib import contextmanager
import sentry_sdk
from quilt import logs

logger = logs.create_logger(__name__)


@contextmanager
def timer(op: str, description: str = None) -> T.Iterator[None]:
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    took_ms = (end - start) * 1_000
    logger.debug(f"{op=}, {description=}, took {took_ms:.3} ms")


@contextmanager
def span(
    op: str,
    description: str = None,
    use_parent: bool = True,
    use: bool = True,
    log: bool = False,
    **kwargs: T.Any,
) -> T.Iterator[T.Any]:
    if not use:
        if log:
            with timer(op=op, description=description):
                yield
        else:
            yield
    else:
        current_span = None
        if use_parent:
            current_span = sentry_sdk.Hub.current.scope.span
        if current_span:
            context = current_span.start_child(op=op, description=description, **kwargs)
        else:
            context = sentry_sdk.start_span(op=op, description=description, **kwargs)
        with context:
            if log:
                with timer(op=op, description=description):
                    yield
            else:
                yield
