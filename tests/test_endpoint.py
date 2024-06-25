import time
from typing import Optional

import pytest
from yiribot.endpoint import Endpoint
from pytest import mark
import asyncio

from yiribot.exceptions import InteralException


@mark.asyncio
async def test_call_endpoint():
    flag = False

    async def ahandler():
        nonlocal flag
        await asyncio.sleep(0.1)
        flag = not flag

    def shandler():
        nonlocal flag
        time.sleep(0.1)
        flag = not flag

    ep = Endpoint(ahandler)

    # 异步
    assert flag is False
    await ep.aexec("")
    assert flag is True

    ep.exec("")

    # 同步
    flag = False
    ep.handler = shandler
    ep.exec("")
    await asyncio.sleep(0.5)
    assert flag is True

    await ep.aexec("")

    s: Optional[str] = None

    async def phandler(echo: str):
        nonlocal s
        s = echo

    ep.handler = phandler
    with pytest.raises(InteralException):
        await ep.aexec("")
    assert s is None
    await ep.aexec("test hello")
    assert s == "hello"
