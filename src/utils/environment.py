import os
import dotenv


class Environment:
    def __init__(self, path: str | os.PathLike):
        dotenv.load_dotenv(path)

        self.api_id = int(os.getenv("API_ID"))
        self.api_hash = os.getenv("API_HASH")
        self.token = os.getenv("TOKEN")
        self.phone = os.getenv("PHONE")


environment = Environment(".env")
