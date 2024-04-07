import time


class InfoStore:
    def __init__(self):
        #self.key_file = key_file
        self.__values = {}

    def delete(self, key):
        del self.__values[key]

    def get(self, key):
        # with open(self.key_file, 'r') as f:
        #     keys = json.load(f)
        values = self.__values.get(key, None)
        if values is None:
            return None
        else:
            return values

    def set(self, key: str, value: dict) -> None:
        self.__values[key] = value
        # with open(self.key_file, 'r') as f:
        #     keys = json.load(f)
        # keys[key_id] = key
        # with open(self.key_file, 'w') as f:
        #     json.dump(keys, f)
