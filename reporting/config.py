import ConfigParser

config = ConfigParser.ConfigParser()
config.read('~/keys.cfg')


def key(key):
    return config.get('CONFIG_KEYS', key)
