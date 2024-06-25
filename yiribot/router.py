import asyncio
from typing import Awaitable, Callable, Dict, Optional, Set, List
import shlex

from mirai_onebot.event import EventBus
from .endpoint import Endpoint
from .utils import develop_logger


class CommandRouter:
    def __init__(self, event_bus: EventBus):
        """将命令路由到Endpoint"""
        self.event_bus = event_bus
        self.command_endpoints: Dict[str, Set[Endpoint]] = {}

    async def execute_command(
        self,
        command: str,
        error_handler: Optional[Callable[[BaseException], Awaitable[None]]] = None,
    ):
        """执行命令，传入原始命令即可。不带 command_prefix 。"""
        endpoints = self.match_endpoint(command)
        try:
            await self.execute_endpoints(command, endpoints)
        except BaseException as e:
            if error_handler is not None:
                await error_handler(e)

    def match_endpoint(self, command: str) -> Set[Endpoint]:
        """匹配 endpoint"""
        command_splited = shlex.split(command)

        endpoints: Optional[Set[Endpoint]] = None
        if command_splited[0] in self.command_endpoints.keys():
            endpoints = self.command_endpoints[command_splited[0]]
        else:
            endpoints = None

        if endpoints is None:
            develop_logger.debug(f"{command} 无法匹配到命令的 Endpoint")
            return set()

        return set(endpoints)

    async def execute_endpoints(self, command: str, endpoints: Set[Endpoint]):
        async_tasks: List[asyncio.Task] = []

        for endpoint in endpoints:
            if endpoint.is_async:
                async_tasks.append(asyncio.create_task(endpoint.aexec(command)))
            else:
                endpoint.exec(command)

        if len(async_tasks) >= 1:
            await asyncio.wait(async_tasks)

    def register_endpoint(self, command: str, endpoint: Endpoint):
        """
        注册命令 Endpoint
        """
        if command in self.command_endpoints.keys():
            self.command_endpoints[command].add(endpoint)
        else:
            self.command_endpoints[command] = set([endpoint])

    def register_function_as_endpoint(self, command: str, handler: Callable):
        """
        将函数注册为 Endpoint，提供一个简化形式。
        """
        endpoint = Endpoint(handler=handler)

        self.register_endpoint(command=command, endpoint=endpoint)
