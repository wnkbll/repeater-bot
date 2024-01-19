from src.bot.routes import start
from src.bot.routes import add

routers = [start.router, add.router]

__all__ = [
    "routers"
]
