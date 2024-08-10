from datetime import time


class TimeValidator:
    def __init__(self, _time: str, separator: str = ","):
        self.time = _time
        self.separator = separator

    def to_string(self) -> str | None:
        try:
            time.fromisoformat(self.time)
            return self.time
        except ValueError:
            return None

    def to_int(self) -> int | None:
        try:
            return int(self.time)
        except ValueError:
            return None

    def to_list(self) -> list[str] | None:
        try:
            times = self.time.split(self.separator)
            for item in times:
                time.fromisoformat(item)

            return times
        except ValueError:
            return None

    def validate_time(self) -> int | list | None:
        time_int = self.to_int()
        if time_int is not None:
            return time_int

        time_list = self.to_list()
        if time_list is not None:
            return time_list

        return None
