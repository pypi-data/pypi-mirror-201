import os
import json


class Config(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            context_root = os.path.dirname(os.path.abspath(__file__))
            config_file = f"{context_root}/config.json"

            with open(config_file, encoding="UTF-8") as json_file:
                self.json_data = json.load(json_file)
                print(f"Loading config.json for [{self.json_data.get('ENV')}] from {config_file}")
            cls._init = True

    def cfg(self, *keys):
        tmp = self.json_data
        try:
            for key in keys:
                tmp = tmp.get(key)
        except Exception as ex:
            print(f"exception : {ex}")
            return None

        return tmp


if __name__ == "__main__":
    x = Config()
    y = Config()

    r = y.cfg("dart", "keys")
    print(r)

    v = x.cfg("message", "telegram", "channel")
    print(v)

    v = x.cfg("crawling_interval")
    print(v)