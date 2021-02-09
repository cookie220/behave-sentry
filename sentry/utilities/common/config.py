from configparser import ConfigParser
import rootpath


class Config(object):

    CONFIG_FILE = rootpath.detect() + "/config.ini"

    @staticmethod
    def get_config():
        cfg = ConfigParser()
        cfg.read(Config.CONFIG_FILE)
        return cfg

    @staticmethod
    def get_config_value(section, key):
        cfg = ConfigParser()
        cfg.read(Config.CONFIG_FILE)
        if cfg.has_section(section):
            if cfg.has_option(section, key):
                return cfg.get(section, key)
            else:
                return None
        else:
            return None

    @staticmethod
    def write_config(section, key, value):
        config = Config.get_config()
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, key, value)
        with open(Config.CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

