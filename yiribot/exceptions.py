class BotException(BaseException):
    def __init__(self, message: str):
        super().__init__(f"Bot 错误: {message}")


__all__ = ["BotException"]
