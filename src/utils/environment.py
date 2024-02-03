import os
import dotenv


class Environment:
    def __init__(self, path: str | os.PathLike):
        dotenv.load_dotenv(path)

        self.api_id: int = int(os.getenv("API_ID"))
        self.api_hash: str = os.getenv("API_HASH")
        self.token: str = os.getenv("TOKEN")
        self.phone: str = os.getenv("PHONE")


environment = Environment("data/.env")
