import random
import sentry_sdk
import typing as T
import functools
from inspect import isawaitable

P = T.ParamSpec("P")


def sample_rate(
    rate: float,
) -> T.Callable[[T.Callable[P, T.Any]], T.Callable[P, T.Any]]:
    def outer_wrapper(func: T.Callable[P, T.Any]) -> T.Callable[P, T.Any]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T.Any:
            with sentry_sdk.configure_scope() as scope:
                scope.transaction.sampled = random.random() < rate
            print("hi there, set this bou")
            result = func(*args, **kwargs)
            if isawaitable(result):
                result = await result
            return result

        return wrapper

    return outer_wrapper
