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


# STRING COLOR

def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return list(tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3)))
    

def get_list_rgb(tuple_str_rgb):
    tuple_rgb = eval(tuple_str_rgb.replace('rgb',''))
    return list(tuple_rgb)


def map_to_GPIOColor(color_str):
    list_color = []
    if '#' in color_str:
        list_color = hex_to_rgb(color_str)
    elif 'rgb' in color_str:
        list_color = get_list_rgb(color_str)
    else:
        return [0, 0, 0]
    colors = []
    for color in list_color:
        colors.append(int((color*100)/255))
    return colors
