# pylint: disable=R0903
from typing import Any

from pydantic import BaseModel
from typing_extensions import Callable, Optional


class Argument(BaseModel):
    """Endpoint 的参数

    Attributes:
        name: 参数名称
        field_info: 列信息
        annotation: 类型标注
    """

    name: str
    annotation: type
    default: Optional[Any] = None
    default_factory: Optional[Callable[[], Any]] = None

    def get_default(self) -> Any | None:
        """获取默认值

        Returns:
            指定 default 时，返回 default 的值；
            指定 default_factory 时，返回 default_factory 的值；
            如果 default 和 default_factory 都没有指定，返回 None；
            如果 default 和 default_factory 都指定，返回 default。
        """

        if self.default is not None:
            return self.default

        if self.default_factory is not None:
            return self.default_factory()

        return None


class AskingArgument(Argument):
    """询问参数，指的是用户执行命令后机器人再询问得出的参数。

    Attributes:
        greeting: 讯问语
    """

    greeting: str


class PositionalArgument(Argument):
    """位置参数，指的是包含在命令里的参数

    Attributes:
        slot: 参数位置
    """

    slot: int

    def get_asking_argument(
        self, greeting: Optional[str] = None
    ) -> AskingArgument:
        return AskingArgument(
            name=self.name,
            annotation=self.annotation,
            greeting=(
                greeting if greeting is not None else f"请输入 {self.name} 的值："
            ),
        )
