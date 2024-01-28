from src.bot.routes import start, add, ls, edit, remove

routers = [start.router, add.router, ls.router, edit.router, remove.router]

__all__ = [
    "routers"
]
