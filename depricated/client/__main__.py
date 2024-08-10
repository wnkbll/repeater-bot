from src.client import Client
from src.utils import environment, Globals


def main():
    config_path = Globals.config_path
    data_path = Globals.data_path

    client = Client(environment.api_id, environment.api_hash, environment.phone, config_path, data_path)
    client.run()


if __name__ == '__main__':
    main()
