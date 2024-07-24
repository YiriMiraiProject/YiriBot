# pylint: disable=C0116
from datetime import datetime, timedelta

from pytest import mark

from yiribot.endpoint import Endpoint, PositionalArgument


@mark.asyncio
async def test_endpoint():
    flag_a: str | None = None

    async def call(test: str):
        nonlocal flag_a
        flag_a = test

    endpoint = Endpoint(
        call, 'test',
        [PositionalArgument(name='test', slot=0, annotation=str)]
    )

    assert flag_a is None
    await endpoint.execute(['hello'])
    assert flag_a == 'hello'

    await endpoint.execute([])
    assert flag_a is None


@mark.asyncio
async def test_endpoint_with_default():
    flag_a: str | None = None

    async def call(test: str):
        nonlocal flag_a
        flag_a = test

    endpoint = Endpoint(
        call, 'test', [
            PositionalArgument(
                name='test', slot=0, annotation=str, default='hello'
            )
        ]
    )

    assert flag_a is None
    await endpoint.execute(['hello2'])
    assert flag_a == 'hello2'

    await endpoint.execute([])
    assert flag_a == 'hello'


@mark.asyncio
async def test_endpoint_with_default_factory():
    flag_a: datetime | None = None

    async def call(test: datetime):
        nonlocal flag_a
        flag_a = test

    endpoint = Endpoint(
        call, 'test', [
            PositionalArgument(
                name='test',
                slot=0,
                annotation=datetime,
                default_factory=datetime.now
            )
        ]
    )

    assert flag_a is None
    await endpoint.execute([datetime(year=2000, month=1, day=1).isoformat()])
    assert flag_a == datetime(year=2000, month=1, day=1)

    await endpoint.execute([])
    assert flag_a is not None
    assert flag_a - datetime.now() < timedelta(minutes=1)


def test_argument_to_asking_argument():
    arg = PositionalArgument(name='a', slot=0, annotation=str)
    assert arg.get_asking_argument().greeting == f'请输入 {arg.name} 的值：'
    assert arg.get_asking_argument('hello').greeting == 'hello'
