from src.bot.routes import start, add, ls, edit, remove, help

routers = [start.router, add.router, ls.router, edit.router, remove.router, help.router]

__all__ = [
    "routers"
]
