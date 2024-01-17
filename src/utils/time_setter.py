from datetime import datetime, time
from pytz import timezone
from tzlocal import get_localzone_name


class TimeSetter:
    @staticmethod
    def is_in_sleep(start: time, stop: time) -> bool:
        current_time = datetime.now().time()
        if stop < start:
            if start <= current_time <= time.fromisoformat("23:59") or time.fromisoformat("00:00") >= current_time >= stop:
                return True

            return False

        if start <= current_time <= stop:
            return True

        return False

    @staticmethod
    def get_interval(sleep: dict[str, str]) -> tuple[time, time]:
        start, stop = time.fromisoformat(sleep["start"]), time.fromisoformat(sleep["stop"])
        return start, stop

    @staticmethod
    def check_timezone(_time: str) -> str:
        moscow = timezone("Europe/Moscow")
        local_timezone = timezone(get_localzone_name())

        if moscow == local_timezone:
            return _time

        local_date = datetime.now().strftime("%Y-%m-%d")
        datetime_string = f"{local_date} {_time}"
        tz = moscow.localize(datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")).astimezone(local_timezone)

        return tz.strftime("%H:%M")
