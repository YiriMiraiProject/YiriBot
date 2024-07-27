import asyncio
import shlex

from yiriob.adapters.base import Adapter
from yiriob.bot import Bot
from yiriob.event.events import GroupMessageEvent

from yiribot.endpoint.base import Endpoint, EndpointCall


class YiriBot(Bot):

    def __init__(
        self, adapter: Adapter, self_id: int, command_prefix: str
    ) -> None:
        super().__init__(adapter, self_id)

        self.command_prefix = command_prefix
        self.command_handlers: dict[str, set[Endpoint]] = {}

        self.bus.subscribe(GroupMessageEvent, self._handle_message)

    async def _handle_message(self, event: GroupMessageEvent) -> None:
        message = event.message.to_cqcode()

        if message.startswith(self.command_prefix):
            command = shlex.split(message[len(self.command_prefix):])
            command[0] = command[0].removeprefix(self.command_prefix)
            await self.handle_command(command)

    async def handle_command(
        self,
        command: list[str],
        background: bool = True,
        timeout: int = 30
    ) -> None:
        """执行命令。原本作为一个内部方法，为了方便测试，将其设为公开方法

        Args:
            command: 命令
            background: 是否后台执行
            timeout: 超时时间，当 background == False 时有效
        """
        # tasks: list[asyncio.Task] = []
        if command[0] in self.command_handlers:
            # for handler in self.command_handlers[command[0]]:
            #     tasks.append(asyncio.create_task(handler.execute(command[1:])))
            tasks: list[asyncio.Task] = [
                asyncio.create_task(handler.execute(command[1:]))
                for handler in self.command_handlers[command[0]]
            ]

            if background:
                await asyncio.wait(tasks, timeout=timeout)

    def register_command_handler(
        self, command: str, handler: EndpointCall
    ) -> None:
        """注册命令处理器

        Args:
            command: 命令
            handler: 命令处理器
        """
        endpoint = Endpoint(
            call=handler, command=command, positional_args=[], asking_args=[]
        )

        if command in self.command_handlers:
            self.command_handlers[command].add(endpoint)
        else:
            self.command_handlers[command] = {endpoint}
