import yaml


class Config:
    configurations = {}

    def load(self, config_file):
        stream = open(config_file, "r")
        self.configurations = yaml.load(stream)

    def get(self, config):
        keys = config.split(".")
        result = self.configurations
        for key in keys:
            result = result[key]

        return result


_config = Config()


def config(key, default=None):
    global _config
    value = None
    try:
        value = _config.get(key)
    except KeyError:
        value = default
    return value


def load(config_file):
    global _config
    _config.load(config_file)