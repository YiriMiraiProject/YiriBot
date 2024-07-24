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
        """
        self.positional_args.sort(key=lambda x: x.slot)

        positional_args = [
            TypeAdapter(argument_signature.field_info.annotation
                        ).validate_python(x) for x, argument_signature in
            zip(raw_positional_args, self.positional_args)
        ]

        await self.call(*positional_args)
