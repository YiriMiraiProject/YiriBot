from typing import Awaitable, Callable, Optional

from pydantic import TypeAdapter

from .argument import AskingArgument, PositionalArgument

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
        self.positional_args = positional_args
        self.asking_args = asking_args

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
