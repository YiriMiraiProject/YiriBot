from typing import Callable
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

        self.bus.subscribe(MessageGroupEvent, self._handle_group_message)
        self.bus.subscribe(MessagePrivateEvent, self._handle_private_message)

    def _handle_group_message(self, event: MessageGroupEvent):
        # TODO: message to str
        event.message.__str__()

    def _handle_private_message(self, event: MessagePrivateEvent):
        pass

    def register_command(self, command: str, handler: Callable):
        pass


__all__ = ["ChatBot"]
