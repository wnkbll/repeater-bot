from src.bot.routes import start, add, ls

routers = [start.router, add.router, ls.router]

__all__ = [
    "routers"
]
