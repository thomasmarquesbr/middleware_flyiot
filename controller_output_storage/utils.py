from flask import make_response
from bson import ObjectId
import ipaddress
import json
import socket
import os


# JSON
def json_response(obj, cls=None):
    response = make_response(json.dumps(obj, cls=cls))
    response.content_type = 'application/json'
    return response
    

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class TransportJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return {k.lstrip('_'): v for k, v in vars(o).items()}


# NETWORK
def is_valid_ip(ip_addr):
    try:
        ipaddress.ip_address(ip_addr)
        return 1
    except:
        return 0


def get_address_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
    # hostname = socket.gethostname()
    # return str(socket.gethostbyname(hostname))


def is_reachable(host):
    return True if os.system("ping -c 1 " + host) is 0 else False
