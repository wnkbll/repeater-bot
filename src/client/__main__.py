from src.client import Client
from src.utils import environment


def main():
    config_path = "data/config.json"
    data_path = "data/data.json"

    client = Client(environment.api_id, environment.api_hash, environment.phone, config_path, data_path)
    client.run()


if __name__ == '__main__':
    main()
