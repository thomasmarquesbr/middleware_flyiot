from utils import *
from const import *
from flask import Flask, jsonify, abort, request
import datetime
from flask_pymongo import PyMongo
from flask_jwt import JWT, jwt_required
from werkzeug.security import safe_str_cmp
import datetime
import sys
import requests

# class User(object):
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password

#     def __str__(self):
#         return "User(id='%s')" % self.id

# users = [
#     User(1, 'user1', 'abcxyz'),
#     User(2, 'user2', 'abcxyz'),
# ]

# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}


ID = sys.argv[1]
PORT = sys.argv[2]

# os.system("python3 register.py " + ID + " " + PORT + " &")
print("Iniciando Data Management Service")
# subprocess.Popen(["python3.5", "register.py"] + [ID, PORT])


user_auth = "user1"
passw_auth = "abcxyz"


def authenticate(username, password):
    if safe_str_cmp(user_auth.encode('utf-8'), username.encode('utf-8')) and safe_str_cmp(passw_auth.encode('utf-8'), password.encode('utf-8')):
        return user_auth
    # user = username_table.get(username, None)
    # if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
    #     return user


def identity(payload):
    user_id = payload['identity']
    return user_id
    # return userid_table.get(user_id, None)


def save_thing(thing):
    if thing['entrypoint']:
        try:
            req = requests.get(thing['entrypoint'], headers=headers)
            info = req.json()
            timestamp = str(datetime.datetime.now())
            thing.update({'timestamp': timestamp})
            for key, item in info.items():
                thing.update({key: item})
        except ConnectionError:
            print("Erro de conexão: "+thing['entrypoint'])
    mongo.db.things.insert_one(thing)


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://{}:{}/{}".format(
    URL_MONGO, PORT_MONGO, DB_MONGO)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)
mongo = PyMongo(app)
jwt = JWT(app, authenticate, identity)

# service = Service("3kwls", "servico1", Service_Type.DATA_MANAGEMENT, '192.168.0.2')


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


@app.route('/protected')
@jwt_required()
def protected():
    return make_response(jsonify({'message': 'Hello World'}), 200)


@app.route('/')
def get_hello():
    return jsonify({'message': 'Hello World'})


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
        result = mongo.db.services.find_one({'id': service_id})
        res = result if result else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/services/search/<service_type>', methods=['GET'])
def get_service_by_type(service_type):
    if not isinstance(service_type, str):
        abort(400)
    else:
        services = [service for service in mongo.db.services.find(
            {'service_type': service_type})]
        return json_response(services, cls=MongoJsonEncoder), 200


@app.route('/services', methods=['POST'])
def add_service():
    service = request.json
    if not service:
        abort(400)
    service_exist = mongo.db.services.find_one({'type': service['type']})
    if service_exist:
        mongo.db.services.update_one({'type': service['type']}, {'$set': service})
    else:
        timestamp = str(datetime.datetime.now())
        service.update({'timestamp': timestamp})
        mongo.db.services.insert_one(service)
    return json_response(service, cls=MongoJsonEncoder), 201


@app.route('/services/<service_id>', methods=['PUT'])
def update_service(service_id):
    service = request.json
    result = mongo.db.services.update_one(
        {'id': service_id}, {'$set': service}
    )
    if result.matched_count > 0:
        return make_response(jsonify({'message': 'Service updated'}), 200)
    else:
        return make_response(jsonify({'message': 'Service not found'}), 404)


@app.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    if not isinstance(service_id, str):
        abort(400)
    else:
        result = mongo.db.services.delete_many({'id': service_id})
        if result.deleted_count is 0:
            abort(404)
        return json_response({'message': 'Service removed successfully'}, cls=MongoJsonEncoder)


@app.route('/services', methods=['DELETE'])
def delete_all_services():
    result = mongo.db.services.delete_many({})
    if not result:
        abort(400)
    return json_response({'message': 'Services removed successfully'}, cls=MongoJsonEncoder)


## THINGS ##
@app.route('/things', methods=['GET'])
def get_things():
    things = [thing for thing in mongo.db.things.find()]
    return json_response(things, cls=MongoJsonEncoder), 200


@app.route('/things/<thing_id>', methods=['GET'])
def get_thing(thing_id):
    if not isinstance(thing_id, str):
        abort(400)
    else:
        result = mongo.db.things.find_one({'id': thing_id})
        res = result if result else {}
        return json_response(res, cls=MongoJsonEncoder), 200


@app.route('/things/search/<thing_name>', methods=['GET'])
def get_thing_by_name(thing_name):
    if not isinstance(thing_name, str):
        abort(400)
    else:
        things = [thing for thing in mongo.db.things.find(
            {'name': thing_name})]
        return json_response(things, cls=MongoJsonEncoder), 200


@app.route('/things', methods=['POST'])
def add_thing():
    thing = request.json
    if not thing:
        abort(400)
    thing_exist = mongo.db.things.find_one({'id': thing['id']})
    if thing_exist:
        make_response({'message', 'Thing alread added'}, 304)
    else:
        save_thing(thing)
        return json_response(thing, cls=MongoJsonEncoder), 201


@app.route('/things/<thing_id>', methods=['PUT'])
def update_thing(thing_id):
    thing = request.json
    result = mongo.db.things.update_one(
        {'id': thing_id}, {'$set': thing}
    )
    if result.matched_count > 0:
        return make_response(jsonify({'message': 'Thing updated'}), 200)
    else:
        return make_response(jsonify({'message': 'Thing not found'}), 404)


@app.route('/things/<thing_id>', methods=['DELETE'])
def delete_thing(thing_id):
    if not isinstance(thing_id, str):
        abort(400)
    else:
        result = mongo.db.things.delete_one({'id': thing_id})
        if result.deleted_count is 0:
            abort(404)
        return json_response({'message': 'Thing removido com sucesso'}, cls=MongoJsonEncoder)


@app.route('/things', methods=['DELETE'])
def delete_all_things():
    result = mongo.db.things.delete_many({})
    if not result:
        abort(400)
    return json_response({'message': 'Things removed successfully'}, cls=MongoJsonEncoder)


# ## DEVICES ##
# @app.route('/devices', methods=['GET'])
# def get_devices():
#     devices = [device for device in mongo.db.devices.find()]
#     return json_response(devices, cls=MongoJsonEncoder), 200
#
#
# @app.route('/devices/<device_id>', methods=['GET'])
# def get_device(device_id):
#     if not isinstance(device_id, str):
#         abort(400)
#     else:
#         result = mongo.db.devices.find_one({'_id': ObjectId(device_id)})
#         res = result if result else {}
#         return json_response(res, cls=MongoJsonEncoder), 200
#
#
# @app.route('/devices', methods=['POST'])
# def add_device():
#     device = request.json
#     if not device:
#         abort(400)
#     mongo.db.devices.insert_one(device)
#     return json_response(device, cls=MongoJsonEncoder), 201
#
#
# @app.route('/devices/<device_id>', methods=['PUT'])
# def update_device(device_id):
#     device = request.json
#     if not device or not isinstance(device_id, str):
#         abort(400)
#     else:
#         result = mongo.db.devices.update_one(
#             {'_id': ObjectId(device_id)}, {'$set': device})
#         device['_id'] = ObjectId(device_id)
#         res = device if result.matched_count > 0 else {}
#         return json_response(res, cls=MongoJsonEncoder), 200
#
#
# @app.route('/devices/<device_id>', methods=['DELETE'])
# def delete_device(device_id):
#     if not isinstance(device_id, str):
#         abort(400)
#     else:
#         result = mongo.db.devices.delete_one({'_id': ObjectId(device_id)})
#         if result.deleted_count is 0:
#             abort(404)
#         return json_response({'message': 'Device removed successfully'}, cls=MongoJsonEncoder)


if __name__ == '__main__':
    try:
        app.run(port=8080)
    except KeyboardInterrupt:
        pass
    finally:
        print("Cancelando a aplicação RESTful...\n")


