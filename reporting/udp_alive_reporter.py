import socket
import config
from threading import Timer

UDP_HOST = (config.key("UDP_REPORTING_HOST"), config.int_key("UDP_REPORTING_PORT"))
TIME_BETWEEN_REPORTS = config.int_key("UDP_SECONDS_BETWEEN_REPORTS")


def report_status(message):
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.sendto(message, UDP_HOST)
    Timer(TIME_BETWEEN_REPORTS, report_status, args=["{}".format(message)]).start()


def start_reporting(message):
    print "UDP_HOST=", UDP_HOST
    print "TIME_BETWEEN_REPORTS", TIME_BETWEEN_REPORTS
    Timer(1, report_status, args=["{}".format(message)]).start()
