import asyncio
import uuid
import asyncer
import shlex
from inspect import Signature, iscoroutinefunction, signature
from typing import Any, Callable, Dict, List, Tuple
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

from yiribot.exceptions import InteralException

from .utils import develop_logger


def get_param_model(command_splited: List[str], signature: Signature) -> BaseModel:
    field_defs: Dict[str, Tuple[Any, FieldInfo]] = {}
    for index, (param_name, param_sign) in enumerate(signature.parameters.items()):
        try:
            field_defs[param_name] = (
                param_sign.annotation,
                FieldInfo(
                    default=command_splited[index + 1], annotation=param_sign.annotation
                ),
            )
        except IndexError:
            raise InteralException("命令缺少参数。")

    return create_model(
        f"DynamicParamModel_{uuid.uuid4()}",
        **field_defs,  # pyright: ignore
    )()


def get_kwargs_from_model(model: BaseModel) -> Dict[str, Any]:
    return model.model_dump()


class Endpoint:
    def __init__(self, handler: Callable) -> None:
        self.handler = handler

    async def _call_handler(self, command: str):
        """
        调用 handler。内部接口
        """
        command_splited = shlex.split(command)

        # 将函数签名解析为参数类型
        param_model = get_param_model(
            command_splited=command_splited, signature=signature(self.handler)
        )

        if self.is_async:
            await self.handler(**get_kwargs_from_model(param_model))
        else:
            await asyncer.asyncify(self.handler)(**get_kwargs_from_model(param_model))

    async def aexec(self, command: str):
        """
        异步执行，会出现等待。
        """
        if not self.is_async:
            develop_logger.debug(
                f"{self.handler} 不是一个异步函数，使用 Endpoint.exec 函数调用"
            )
            return

        await self._call_handler(command)

    def exec(self, command: str):
        """
        同步执行。不阻塞。
        """
        if self.is_async:
            develop_logger.debug(
                f"{self.handler} 不是一个同步函数，使用 Endpoint.aexec 函数调用"
            )
            return

        asyncio.create_task(self._call_handler(command))

    @property
    def is_async(self):
        return iscoroutinefunction(self.handler)


__all__ = ["Endpoint"]
