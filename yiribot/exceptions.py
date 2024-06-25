class BaseBotException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BotException(BaseBotException):
    def __init__(self, message: str):
        super().__init__(f"Bot 错误: {message}")


class InteralException(BaseBotException):
    def __init__(self, message: str) -> None:
        super().__init__(f"YiriBot 框架错误：{message}")


__all__ = ["BotException", "InteralException", "BaseBotException"]
