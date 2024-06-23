# isort: off
# autopep8: off
import sys

sys.path.append("..")

from yiribot import ChatBot  # noqa: E402
from YiriOneBot.mirai_onebot import ReverseWebsocketAdapter  # noqa: E402
# isort: on
# autopep8: on


bot = ChatBot(
    adapter=ReverseWebsocketAdapter(
        host="127.0.0.1", port=8120, timeout=10, access_token="access_token"
    ),
    command_prefix=".",
)


@bot.on_command("hello")
async def handle_hello(message: str):
    print("handle command hello")
    print(f"{message}")

    await bot.send_private_message("2389472915", "Hello World")


bot.run()
