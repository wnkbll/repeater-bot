from src.lang import ru, en, debug

STRINGS = {}

STRINGS = ru.register(STRINGS)
STRINGS = en.register(STRINGS)
STRINGS = debug.register(STRINGS)

__all__ = [
    "STRINGS"
]
