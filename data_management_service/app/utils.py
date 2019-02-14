from flask import make_response
from bson import ObjectId
import ipaddress
import json



## JSON ##
def json_response(obj, cls=None):
    response = make_response(json.dumps(obj, cls=cls))
    response.content_type = 'application/json'
    return response
    

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


## NETWORK ##
def is_valid_ip(ip_addr):
    try:
        ipaddress.ip_address(ip_addr)
        return 1
    except:
        return 0