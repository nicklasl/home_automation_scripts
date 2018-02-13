import Adafruit_DHT

sensor_type = Adafruit_DHT.DHT22


def read_temp_and_humidity(gpio):
    humidity, temperature = Adafruit_DHT.read_retry(sensor_type, gpio)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        None
