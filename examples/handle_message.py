from yiribot import ChatBot  # noqa: E402
from mirai_onebot import ReverseWebsocketAdapter  # noqa: E402


bot = ChatBot(
    adapter=ReverseWebsocketAdapter(
        host="127.0.0.1", port=8120, timeout=10, access_token="access_token"
    ),
    command_prefix=".",
)


@bot.on("hello")
def handle_hello():
    print("hello")


bot.run()
