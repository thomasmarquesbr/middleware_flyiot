import sys
from const import *
from flask import Flask, jsonify, make_response, abort, request
from controller import ThingController


ID = sys.argv[1]
PORT = sys.argv[2]

print("Iniciando Interface")

app = Flask(__name__)
app.debug = DEBUG

thing = ThingController()


## DEFAULT ##
@app.route('/', methods=['GET'])
def get_hello():
    info = {
        'events': ['isCreated', 'isModified', 'isDeleted']
    }
    return make_response(jsonify(info), 200)


@app.route('/data_management', methods=['POST'])
def add_data_management():
    info = request.json
    if 'entrypoint' in info:
        data_management = info['entrypoint']
        thing.set_data_management(data_management)
    return make_response(jsonify({'message': 'data_management added'}), 200)


@app.route('/actions', methods=['PUT'])
def action_turn():
    global thing
    actions = request.json
    result = thing.actions(actions)
    if result:
        if 'message' in result.keys():
            return make_response(jsonify({'message': 'Action registered'}), 200)
        elif 'data' in result.keys():
            return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify({'message': 'Action doesn\'t exist'}), 404)


@app.route('/obervables', methods=['PUT'])
def observe():
    global thing
    json = request.json
    thing.observe(json)
    return make_response({'message': 'Observable registered'}, 200)


def notify_event(event):
    print("Evento aconteceu")


if __name__ == '__main__':
    try:
        if DEBUG:
            app.run(port=int(PORT))
        else:
            app.run(host='0.0.0.0', port=int(PORT))
    except KeyboardInterrupt:
        pass
    finally:
        print("Cancelando a aplicação RESTful...\n")
