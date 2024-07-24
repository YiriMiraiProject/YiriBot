# pylint: disable=R0903
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from typing_extensions import Optional


class Argument(BaseModel):
    """Endpoint 的参数

    Attributes:
        name: 参数名称
        field_info: 列信息
        annotation: 类型标注
    """

    name: str
    field_info: FieldInfo


class AskingArgument(Argument):
    """询问参数，指的是用户执行命令后机器人再询问得出的参数。

    Attributes:
        greeting: 讯问语
    """

    greeting: FieldInfo


class PositionalArgument(Argument):
    """位置参数，指的是包含在命令里的参数

    Attributes:
        slot: 参数位置
    """

    slot: int

    def get_asking_argument(
        self, greeting: Optional[FieldInfo] = None
    ) -> AskingArgument:
        return AskingArgument(
            name=self.name,
            field_info=self.field_info,
            greeting=(
                greeting if greeting is not None else
                Field(default=f"请输入 {self.name} 的值：")
            ),
        )
