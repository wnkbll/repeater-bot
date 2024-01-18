from src.lang import ru
from src.lang import en
from src.lang import debug

STRINGS = {}

STRINGS = ru.register(STRINGS)
STRINGS = en.register(STRINGS)
STRINGS = debug.register(STRINGS)

__all__ = [
    "STRINGS"
]
