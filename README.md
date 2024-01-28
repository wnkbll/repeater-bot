### Запуск на Linux
 + `python -m venv venv` - создание виртуального окружения;
 + `source venv/bin/activate` - активация виртуального окружения;
 + `python -m pip install --upgrade pip wheel setuptools` - обновление пакетов `pip`, `wheel` и `setuptools`;
 + `pip install -e .` - установка зависимостей;
 + `python -m src.bot` - запуск бота;
 + `python -m src.client` - запуск клиента.


### Запуск на Windows
 + `python -m venv venv` - создание виртуального окружения;
 + `venv/Scripts/activate` - активация виртуального окружения;
 + `python.exe -m pip install --upgrade pip wheel setuptools` - обновление пакетов `pip`, `wheel` и `setuptools`;
 + `pip install -e .` - установка зависимостей;
 + `python -m src.bot`  - запуск бота;
 + `python -m src.client` - запуск клиента.


### Screen (Linux)
 + `screen -S [name]` - запуск нового окна с именем `name`;
 + `Ctrl + A + D` - свернуть текущее окно;
 + `screen -r [name]` - развернуть окно с именем `name`;
 + `screen -ls` - список всех окон.


### Структура файла `.env`
 ```
 API_ID: int
 API_HASH: str
 TOKEN: str
 PHONE: str
 ```


### Структура файла `config.json`
 ```
 {
    "white_list": list[int],
    "chats": dict[str, int | list[str]],
    "sleep": dict[str, str]
 }
 ```

 *Пример:*
  ```
  {
    "white_list": [
        -123456789, 987654321
    ],
    "chats": {
        "t.me/link1": ["10:00", "14:30", "19:00"],
        "t.me/link2": 60,
        "t.me/link3": ["08:15", "22:22"],
        "t.me/link4": 100
    },
    "sleep": {
        "start": "17:00",
        "stop": "20:00"
    }
}
  ```
 + В `"white_list"` записываются ID пользователей, с которыми разрешено взаимодействовать боту.
 + В `"chats"` ключом является ссылка на чат, значением - интервал между рассылкой(в минутах) или список часов в формате `HH:MM`, в которые ежедневно рассылаются сообщения.
 + В `"sleep"` к ключам `start` и `stop` указывается время в формате `HH:MM`, между которыми рассылка будет приостановлена.

### ToDo
 - [x] Редактирование `config.json` через `bot.py`;
 - [x] Возможность указывать конкретное время в `config.py`;