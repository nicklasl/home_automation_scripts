import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/home/pi/keys.cfg')


def key(key):
    return config.get('CONFIG_KEYS', key)
