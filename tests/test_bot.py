# pylint: disable=W0621,C0116
import asyncio
from typing import Optional

from pytest import fixture, mark
from yiriob.adapters import ReverseWebsocketAdapter
from yiriob.event import EventBus

from yiribot.bot import YiriBot


@fixture(scope="module")
def bot():
    bot = YiriBot(
        adapter=ReverseWebsocketAdapter(
            host="127.0.0.1", port=8080, access_token='hello', bus=EventBus()
        ),
        self_id=1,
        command_prefix="."
    )

    bot.adapter.start()
    yield bot
    bot.adapter.stop()


@mark.asyncio
async def test_handle_command(bot: YiriBot):
    flag_a: Optional[str] = None

    async def handler(name: str):
        nonlocal flag_a
        flag_a = f'hello {name}'

    bot.register_command_handler('say_hello', handler)

    assert flag_a is None
    await bot.handle_command(['.say_hello', 'xiaoming'], background=False)
    await asyncio.sleep(0.1)
    assert flag_a == 'hello xiaoming'
