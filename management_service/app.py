import signal
import subprocess
import sys
import time

from flask import Flask, jsonify, abort, request

from const import *
from util import *


def signal_handling(signum, frame):
    print("Encerrando Management Service ("+ID+")")
    global process
    if process:
        process = None
    sys.exit()


print("Iniciando Management Service")

ID = sys.argv[1]
PORT = sys.argv[2]

run_monitoring = True
data_management_service = None
process = None

app = Flask(__name__)
if DEBUG:
    app.debug = True

signal.signal(signal.SIGINT, signal_handling)

headers = {
    # 'Authorization' : ‘(some auth code)’,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


@app.route('/')
def get_hello():
    return jsonify({'message': 'Hello! I am ' + SERVICE_TYPE})


@app.route('/data_management', methods=['POST'])
def add_data_management():
    info = request.json
    if "entrypoint" in info:
        global data_management_service
        global process
        if process:
            process = None
        data_management_service = info["entrypoint"]
        subprocess.Popen(["python3.7", "monitor.py"] + [data_management_service])
        return json_response({'message': 'data_management added successfuly'})
    else:
        abort(400)


def finish():
    print("Cancelando a aplicação RESTful...\n")


# def run(running):
#     while True:
#         print('monitor is running')
#         if data_management_service:
#             req = requests.get(data_management_service+"services")
#             services = req.json()
#             if services:
#                 print(services)
#         time.sleep(10)
#         if running():
#             break


def run():
    while True:
        print(data_management_service)
        # if data_management_service:
        #     req = requests.get(str(data_management_service), headers=headers)
        #     print(req.json())
        time.sleep(5)
        global stop_threads
        if stop_threads:
            break


if __name__ == '__main__':
    try:
        # stop_threads = False
        # t1 = threading.Thread(target=run)
        # t1.start()
        # time.sleep(1)
        if DEBUG:
            app.run(port=int(PORT))
        else:
            app.run(host='0.0.0.0', port=int(PORT))
    except KeyboardInterrupt:
        pass
    finally:
        finish()
