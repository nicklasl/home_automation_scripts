#!/usr/bin/python
# coding=utf-8
import os
import sys
# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import smtplib
from email.mime.text import MIMEText
import influxdb
import config
import logging
from subprocess import call

LIMIT = 1500
PUSH_NOTIFICATION_FILE_NAME = "send_push.sh"


def setup_logging():
    global logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(message)s', filename='alarm.log', level=logging.INFO)
    logging.getLogger(__name__).setLevel(logging.DEBUG)


def setup_influx_client():
    global client
    INFLUX_URI = config.key("INFLUX_URI")
    INFLUX_USERNAME = config.key("INFLUX_USERNAME")
    INFLUX_PASSWORD = config.key("INFLUX_PASSWORD")
    INFLUX_DATABASE = config.key("INFLUX_DATABASE")
    client = influxdb.InfluxDBClient(INFLUX_URI, 8086, INFLUX_USERNAME, INFLUX_PASSWORD, INFLUX_DATABASE)


def send_warning_email(message):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config.key('GMAIL_LOGIN'), config.key('GMAIL_APP_PASSWORD'))

    sender = config.key('GMAIL_FROM_ADDRESS')
    msg = MIMEText("""{}""".format(message))
    recipients = [config.key('GMAIL_TO_ADDRESS1'), config.key('GMAIL_TO_ADDRESS2')]
    msg['Subject'] = "Kolla värmepumpen"
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    server.sendmail(sender, recipients, msg.as_string())
    server.quit()


def main():
    result = client.query('select sum(value) from electricity where time > now() - 15m')
    dict = result.raw
    watts_last_15m = dict[u'series'][0][u'values'][0][1]
    print watts_last_15m
    if watts_last_15m > LIMIT:
        message = "Huset drog {} W senaste 15 minutrarna. Gränsen är {} W".format(watts_last_15m, LIMIT)
        logger.warn(message)
        send_warning_email(message)
        if os.path.isfile(PUSH_NOTIFICATION_FILE_NAME):
            call(['bash', PUSH_NOTIFICATION_FILE_NAME, message])
    else:
        logger.debug("Consumed last 15 min: {} W".format(watts_last_15m))


setup_logging()
setup_influx_client()

main()
