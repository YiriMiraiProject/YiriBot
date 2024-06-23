from typing import Callable, Dict, Set, Union
import shlex
from mirai_onebot import Bot, MessagePrivateEvent, MessageGroupEvent
from mirai_onebot.adapters.base import Adapter


class ChatBot(Bot):
    def __init__(
        self,
        adapter: Adapter,
        bot_platform: str,
        bot_user_id: str,
        command_prefix: str = ".",
    ):
        """
        聊天机器人类。
        """

        self.command_prefix = command_prefix

        self.command_handlers: Dict[str, Set[Callable]] = {}

        self.bus.subscribe(MessageGroupEvent, self._handle_message)
        self.bus.subscribe(MessagePrivateEvent, self._handle_message)

    def _handle_message(self, event: Union[MessageGroupEvent, MessagePrivateEvent]):
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

    def register_command(self, command: str, handler: Callable):
        pass


__all__ = ["ChatBot"]
