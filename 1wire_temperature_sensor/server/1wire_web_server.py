import os
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    if os.getuid() != 0:
        print "This server needs to be run as root. Sorry!"
        exit(1)
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    app.run()