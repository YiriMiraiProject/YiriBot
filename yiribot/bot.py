from typing import Callable, Dict, Optional, Set, Union
import shlex
from mirai_onebot import Bot, MessagePrivateEvent, MessageGroupEvent
from mirai_onebot.adapters.base import Adapter
from yiribot.utils import develop_logger
import asyncio


class ChatBot(Bot):
    def __init__(
        self,
        adapter: Adapter,
        bot_platform: Optional[str] = None,
        bot_user_id: Optional[str] = None,
        command_prefix: str = ".",
    ):
        """
        聊天机器人类。
        """
        super().__init__(
            adapter=adapter,
            bot_platform=bot_platform,
            bot_user_id=bot_user_id,
        )

        self.command_prefix = command_prefix

        self.command_handlers: Dict[str, Set[Callable]] = {}

        self.bus.subscribe(MessageGroupEvent, self._handle_message)
        self.bus.subscribe(MessagePrivateEvent, self._handle_message)

    async def _handle_message(
        self, event: Union[MessageGroupEvent, MessagePrivateEvent]
    ):
        """
        处理消息。
        """
        if str(event.message).startswith(self.command_prefix):
            self._match_command_handler(
                str(event.message).removeprefix(self.command_prefix)
            )

    def _match_command_handler(self, command: str):
        """
        匹配命令及其处理器。
        输入的命令不带 command_prefix。
        """
        splited = shlex.split(command)

        handlers = self.command_handlers.get(splited[0], None)

        if handlers is None:
            return

        for handler in handlers:
            asyncio.get_event_loop().create_task(handler(command[1:]))

    def register_command(self, command: str, handler: Callable):
        """
        注册命令。
        """
        if command.startswith(self.command_prefix):
            develop_logger.warning(
                f"command 参数不能含有命令前缀: {self.command_prefix}"
            )
            return

        if command in self.command_handlers.keys():
            self.command_handlers[command].add(handler)
        else:
            self.command_handlers[command] = set([handler])

    def on_command(self, command: str):
        """
        注册命令，装饰器函数样式。
        """

        def wrapper(func: Callable):
            self.register_command(command, func)

            def inner():
                func()

            return inner

        return wrapper


__all__ = ["ChatBot"]
