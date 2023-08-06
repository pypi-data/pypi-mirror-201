import typing as T
import random


class TracesException(Exception):
    def __init__(
        self, message: T.Optional[str] = "", traces_rate: T.Optional[float] = 1
    ):
        """
        :param message: the error message to display to the user
        :param traces_rate: the traces rate for Sentry, between 0 and 1, inclusive
        """
        self.message = message
        self.traces_rate = traces_rate
        super().__init__(self.message)

    def should_capture(self) -> bool:
        if self.traces_rate == 1:
            return True
        if self.traces_rate == 0:
            return False
        return random.random() < self.traces_rate


class DisplayException(TracesException):
    @classmethod
    def which_exception(cls, e: Exception) -> Exception:
        str_e = str(e)
        if str_e.startswith("*"):
            return cls(message=str_e[1:])
        return e
