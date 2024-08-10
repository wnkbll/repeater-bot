class Dictionaries:
    @staticmethod
    def compare_dictionaries(previous: dict, current: dict) -> tuple[list, list]:
        previous_keys = previous.keys()
        current_keys = current.keys()

        added_keys = []
        deleted_keys = []

        if previous_keys != current_keys:
            for key in previous_keys:
                if key not in current:
                    deleted_keys.append(key)

            for key in current_keys:
                if key not in previous:
                    added_keys.append(key)

        return added_keys, deleted_keys

    @staticmethod
    def get_key(dictionary: dict, index: int) -> str:
        for i, key in enumerate(dictionary.keys()):
            if i == index:
                return key
