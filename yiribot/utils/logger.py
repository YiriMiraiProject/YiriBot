import logging
from rich.logging import RichHandler

logging.basicConfig(level=logging.DEBUG, handlers=[RichHandler()])

core_logger = logging.getLogger("YiriBot Core")
develop_logger = logging.getLogger("YiriBot Deveolp")

__all__ = ["core_logger", "develop_logger"]
