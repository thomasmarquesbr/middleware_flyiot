from flask import Flask, jsonify, abort, request, make_response
from flask_pymongo import PyMongo
from dao import ThingsDao, ServicesDao
from bson import ObjectId
from config import *
import json


def json_response(obj, cls=None):
    response = make_response(json.dumps(obj, cls=cls))
    response.content_type = 'application/json'
    return response
    

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

app = Flask(__name__)

thingsDao = ThingsDao()
servicesDao = ServicesDao()
app.config["MONGO_URI"] = "mongodb://{}:{}/{}".format(URL_MONGO, PORT_MONGO, DB_MONGO)
mongo = PyMongo(app)


# @auth.error_handler
# def unauthorized():
#     # return 403 instead of 401 to prevent browsers from displaying the default
#     # auth dialog
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/hello')
def get_services():
    return jsonify({'message': 'Hello World'})


## RESOURCES ##
@app.route('/resources', methods=['GET'])
def get_resources():
    resources = [resource for resource in mongo.db.resources.find()]
    return json_response(resources, cls=MongoJsonEncoder), 200


@app.route('/resources/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    if not isinstance(resource_id, str):
        abort(400)
    else:
        result = mongo.db.resources.find_one({'_id': ObjectId(resource_id)})
        res = result if result else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/resources/<resource_name>', methods=['GET'])
def get_resource_by_name(resource_name):
    if not isinstance(resource_name, str):
        abort(400)
    else:
        resources = [resource for resource in mongo.db.resources.find({'_id': ObjectId(resource_id)})]
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/resources', methods=['POST'])
def add_resource():
    resource = request.json
    if not resource:
        abort(400)
    mongo.db.resources.insert_one(resource)
    return json_response(resource, cls=MongoJsonEncoder), 201


@app.route('/resources/<resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = request.json
    if not resource or not isinstance(resource_id, str):
        abort(400)
    else:
        result = mongo.db.resources.update_one({'_id': ObjectId(resource_id)}, {'$set': resource})              
        resource['_id'] = ObjectId(resource_id)
        res = resource if result.matched_count > 0 else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/resources/<resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    if not isinstance(resource_id, str):
        abort(400)
    else:
        result = mongo.db.resources.delete_one({'_id': ObjectId(resource_id)})
        if result.deleted_count is 0: 
            abort(404)
        return json_response({'message': 'Device removed successfully'}, cls=MongoJsonEncoder)


## DEVICES ##
@app.route('/devices', methods=['GET'])
def get_devices():
    devices = [device for device in mongo.db.devices.find()]
    return json_response(devices, cls=MongoJsonEncoder), 200


@app.route('/devices/<device_id>', methods=['GET'])
def get_device(device_id):
    if not isinstance(device_id, str):
        abort(400)
    else:
        result = mongo.db.devices.find_one({'_id': ObjectId(device_id)})
        res = result if result else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/devices', methods=['POST'])
def add_device():
    device = request.json
    if not device:
        abort(400)
    mongo.db.devices.insert_one(device)
    return json_response(device, cls=MongoJsonEncoder), 201


@app.route('/devices/<device_id>', methods=['PUT'])
def update_device(device_id):
    device = request.json
    if not device or not isinstance(device_id, str):
        abort(400)
    else:
        result = mongo.db.devices.update_one({'_id': ObjectId(device_id)}, {'$set': device})              
        device['_id'] = ObjectId(device_id)
        res = device if result.matched_count > 0 else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    if not isinstance(device_id, str):
        abort(400)
    else:
        result = mongo.db.devices.delete_one({'_id': ObjectId(device_id)})
        if result.deleted_count is 0: 
            abort(404)
        return json_response({'message': 'Device removed successfully'}, cls=MongoJsonEncoder)


if __name__ == '__main__':
    app.run(port=8080, debug=True)