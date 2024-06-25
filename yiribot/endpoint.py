from inspect import isawaitable
from typing import Callable
from .utils import develop_logger


class Endpoint:
    def __init__(self, handler: Callable) -> None:
        self.handler = handler

    async def aexec(self):
        if not self.is_async:
            develop_logger.debug(
                f"{self.handler} 不是一个异步函数，使用 Endpoint.exec 函数调用"
            )
            return

        await self.handler()

    def exec(self):
        if self.is_async:
            develop_logger.debug(
                f"{self.handler} 不是一个同步函数，使用 Endpoint.aexec 函数调用"
            )
            return

        self.handler()

    @property
    def is_async(self):
        return isawaitable(self.handler)


__all__ = ["Endpoint"]
