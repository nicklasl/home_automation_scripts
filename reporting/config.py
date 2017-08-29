import ConfigParser

config = ConfigParser.ConfigParser()
config.read('~/keys.cfg')


def key(key):
    return config.get('CONFIG_KEYS', key)


def int_key(key):
    return config.getint('CONFIG_KEYS', key)
