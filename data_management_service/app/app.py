from flask import Flask, jsonify, abort, request, make_response
from flask_pymongo import PyMongo
from bson import ObjectId
import json

from utils import json_response, MongoJsonEncoder, TransportJsonEncoder
from config import *
from models import Service, Service_Type



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://{}:{}/{}".format(URL_MONGO, PORT_MONGO, DB_MONGO)
mongo = PyMongo(app)

service = Service("3kwls", "servico1", Service_Type.DATA_MANAGEMENT, '192.168.0.2')


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
def get_hello():
    return jsonify({'message': 'Hello World'})


## SERVICES ##


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


@app.route('/resources/search/<resource_name>', methods=['GET'])
def get_resource_by_name(resource_name):
    if not isinstance(resource_name, str):
        abort(400)
    else:
        resources = [resource for resource in mongo.db.resources.find({'name': resource_name})]
        return json_response(resources, cls=MongoJsonEncoder), 200


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
        return json_response({'message': 'Resource removed successfully'}, cls=MongoJsonEncoder)


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


## SERVICES ##
@app.route('/services', methods=['GET'])
def get_services():
    services = [service for service in mongo.db.services.find()]
    return json_response(services, cls=MongoJsonEncoder), 200


@app.route('/services/<service_id>', methods=['GET'])
def get_service(service_id):
    if not isinstance(service_id, str):
        abort(400)
    else:
        result = mongo.db.services.find_one({'_id': ObjectId(service_id)})
        res = result if result else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/services/search/<service_type>', methods=['GET'])
def get_service_by_type(service_type):
    if not isinstance(service_type, str):
        abort(400)
    else:
        services = [service for service in mongo.db.services.find({'service_type': service_type})]
        return json_response(services, cls=MongoJsonEncoder), 200


@app.route('/services', methods=['POST'])
def add_service():
    service = request.json
    if not service:
        abort(400)
    mongo.db.services.insert_one(service)
    return json_response(service, cls=MongoJsonEncoder), 201


@app.route('/services/<service_id>', methods=['PUT'])
def update_service(service_id):
    service = request.json
    if not service or not isinstance(service_id, str):
        abort(400)
    else:
        result = mongo.db.services.update_one({'_id': ObjectId(service_id)}, {'$set': service})              
        service['_id'] = ObjectId(service_id)
        res = service if result.matched_count > 0 else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    if not isinstance(service_id, str):
        abort(400)
    else:
        result = mongo.db.services.delete_one({'_id': ObjectId(service_id)})
        if result.deleted_count is 0: 
            abort(404)
        return json_response({'message': 'Service removed successfully'}, cls=MongoJsonEncoder)


if __name__ == '__main__':
    app.run(port=8080, debug=True)