from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone_name


class TimeSetter:
    @staticmethod
    def is_in_sleep(start: int, stop: int, is_dif_days: bool) -> bool:
        current_time = datetime.now().time().hour * 60 + datetime.now().time().minute

        if is_dif_days:
            if start <= current_time <= 1439 or 0 >= current_time >= stop:
                return True

            return False

        if start <= current_time <= stop:
            return True

        return False

    @staticmethod
    def convert_time(time_string: str) -> int:
        if time_string.strip() == "":
            return 0

        return int(time_string[:time_string.find(":")]) * 60 + int(time_string[time_string.find(":") + 1:])

    @staticmethod
    def get_interval(sleep: dict[str, str]) -> tuple:
        time_start, time_stop = TimeSetter.convert_time(sleep["start"]), TimeSetter.convert_time(sleep["stop"])

        return time_start, time_stop

    @staticmethod
    def check_timezone(time: str) -> str:
        moscow = timezone("Europe/Moscow")
        local_timezone = timezone(get_localzone_name())

        if moscow == local_timezone:
            return time

        local_date = datetime.now().strftime("%Y-%m-%d")
        datetime_string = f"{local_date} {time}"
        tz = moscow.localize(datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")).astimezone(local_timezone)

        return tz.strftime("%H:%M")
