import os
import json
import time
from flask import Flask, abort

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def restart():
    os.system('pm2 restart node-red')
    return "OK"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
