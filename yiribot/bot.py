import asyncio
from typing import Optional, Callable, Union
from mirai_onebot import Bot
from mirai_onebot.adapters.base import Adapter
from mirai_onebot.event import MessageGroupEvent, MessagePrivateEvent
from .router import CommandRouter
from .utils import develop_logger


class ChatBot:
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
        self.adapter = adapter
        self.command_prefix = command_prefix
        self._bot = Bot(
            adapter=adapter, bot_user_id=bot_user_id, bot_platform=bot_platform
        )

        self.router = CommandRouter(event_bus=self._bot.bus)

        self._bot.subscribe(MessagePrivateEvent, self._on_message_received)
        self._bot.subscribe(MessageGroupEvent, self._on_message_received)

    async def _error_handler(
        self,
        exception: BaseException,
        event: Union[MessageGroupEvent, MessagePrivateEvent],
    ) -> None:
        exception_string = f"🚨 {str(exception)}"

        if isinstance(event, MessageGroupEvent):
            await self._bot.send_group_message(
                group_id=event.group_id,
                message=exception_string,
            )
        elif isinstance(event, MessagePrivateEvent):
            await self._bot.send_private_message(
                user_id=event.user_id, message=exception_string
            )

        develop_logger.exception(exception)

    async def _on_message_received(
        self, event: Union[MessagePrivateEvent, MessageGroupEvent]
    ):
        message = str(event.message)

        if message.startswith(self.command_prefix):
            asyncio.create_task(
                self.router.execute_command(
                    message.removeprefix(self.command_prefix),
                    event=event,
                    error_handler=self._error_handler,
                )
            )

    def register_function_as_endpoint(self, command: str, handler: Callable):
        if command.startswith(self.command_prefix):
            develop_logger.warning(
                "注册 Endpoint 时的命令带有 command_prefix，可能不会被识别。"
            )

        return self.router.register_function_as_endpoint(
            command=command, handler=handler
        )

    def on(self, command: str):
        def wrapper(func: Callable):
            self.register_function_as_endpoint(command, func)
            return func

        return wrapper

    def run(self):
        self._bot.run()


__all__ = ["ChatBot"]
