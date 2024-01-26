from src.bot.routes import start, add, ls, edit

routers = [start.router, add.router, ls.router, edit.router]

__all__ = [
    "routers"
]
