from flask import Flask, jsonify, abort, request, make_response
import discovery_service.discovery as discovery
import os
import uuid
import socket
import requests
import subprocess


ID = str(uuid.uuid1())
PORT = str(5000)


# req = requests.post("http://localhost:8080/services", json={"teste": "teste"})
# print(req.json())

# os.system("python3 register.py " + ID + " " + PORT + " &")
subprocess.Popen(["python3.5", "register.py"] + [ID, PORT])
# os.system("python3 discovery.py ")
subprocess.Popen(["python3.5", "discovery.py"])


# old = Flask(__name__)
# old.debug = True
#
#
# @old.route('/services')
# def get_services():
#     return discovery.services_on
#
#
# @old.route('/hello')
# def hello():
#     return make_response(jsonify({'message': 'Hello World'}), 200)
#
#
# if __name__ == '__main__':
#     old.run(port=8080)


# import os
