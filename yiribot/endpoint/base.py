from inspect import Parameter, signature
from typing import (
    Annotated, Any, Awaitable, Callable, Optional, get_args, get_origin
)

from pydantic import TypeAdapter

from .argument import AskingArgument, PositionalArgument
from .params import AskingArgumentParam

EndpointCall = Callable[..., Awaitable[None]]


class Endpoint:

    def __init__(
        self,
        call: EndpointCall,
        command: str,
        positional_args: Optional[list[PositionalArgument]] = None,
        asking_args: Optional[list[AskingArgument]] = None,
    ) -> None:
        if positional_args is None:
            positional_args = []

        if asking_args is None:
            asking_args = []

        self.call = call
        self.command = command
        self.positional_args = positional_args if positional_args else self.get_positional_args(
        )
        self.asking_args = asking_args

    def get_positional_args(self) -> list[PositionalArgument]:
        """从 self.call 获取 PositionalArguments。

        Returns:
            获取到的 PositionalArguments
        """
        sign = signature(self.call)
        params = sign.parameters

        positional_args: list[PositionalArgument] = []

        for index, (name, param) in enumerate(params.items()):
            anno: Any = param.annotation

            if anno is Parameter.empty:
                anno = Any

            if get_origin(anno) is Annotated:
                if AskingArgumentParam() in get_args(anno):
                    continue

            positional_args.append(
                PositionalArgument(
                    name=name,
                    annotation=anno,
                    default=param.default,
                    slot=index
                )
            )

        return positional_args

    async def execute(self, raw_positional_args: list[str]) -> None:
        """执行该 Endpoint

        Args:
            raw_positional_args: 原始的 positional_args，不包含 self.command

        Raises:
            pydantic.ValidationError: 参数类型验证错误
        """
        self.positional_args.sort(key=lambda x: x.slot)

        positional_args = []

        for index, argument_signature in enumerate(self.positional_args):
            try:
                positional_args.append(
                    TypeAdapter(argument_signature.annotation
                                ).validate_python(raw_positional_args[index])
                )
            except IndexError:
                positional_args.append(argument_signature.get_default())

        await self.call(*positional_args)
