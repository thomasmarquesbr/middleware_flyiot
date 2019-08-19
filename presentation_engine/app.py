import sys
import uuid

import requests
from const import *
from FlyIoTLParser import *
from flask import Flask, jsonify, abort, request
from utils import *

ID = sys.argv[1]
PORT = sys.argv[2]
filepath = sys.argv[3]
data_management_service = None
parser = None
type_things_discovered = []
workflows = {}

app = Flask(__name__)
if DEBUG:
    app.debug = True


def subscribe_events():
    global parser
    global type_things_discovered
    global data_management_service
    global workflows

    things = parser.things
    workflows = parser.workflows
    group_events = []
    for name, workflow in workflows.copy().items():
        # print('name: '+name)
        for i, item in enumerate(workflow['when']):
            # print(str(i)+' '+str(item))
            for key, value in item.copy().items():
                event_id = str(uuid.uuid1())+'_'+name+'_'+'when'+'_'+str(i)+'_'+key
                workflows[name]['when'][i]['status'] = False
                # group_events[event_id] = value
                if key in things.keys():
                    group_events.append({
                        'id': event_id,
                        'condition': value,
                        'thing': things[key]['type']
                    })
                else:
                    group_events.append({
                        'id': event_id,
                        'condition': value,
                        'workflow': key
                    })

    if len(group_events) > 0:
        try:
            req = requests.put(data_management_service+'events', json=group_events, headers=headers)
            print(req.json())
        except requests.ConnectionError:
            print("Erro de conexão: "+data_management_service+"events")
    # print(json.dumps(group_events, indent=2))


if filepath:
    parser = FlyIoTLParser(filepath)
    parser.syntax_validate()
    parser.semantic_validate()


def get_types_discovered():
    try:
        req = requests.get(data_management_service+'types', headers=headers)
        return req.json()
    except requests.ConnectionError:
        print("Erro de conexão: " + str(data_management_service) + 'types')
        return []


@app.route('/', methods=['GET'])
def get_hello():
    return jsonify({'message': 'Hello World'})


@app.route('/data_management', methods=['POST'])
def add_data_management():
    info = request.json
    if "entrypoint" in info:
        global data_management_service
        global type_things_discovered
        data_management_service = info["entrypoint"]
        type_things_discovered = get_types_discovered()
        subscribe_events()
        return json_response({'message': 'data_management added successfuly'})
    else:
        abort(400)


@app.route('/notification/<event_id>', methods=['PUT'])
def notification(event_id):
    print(event_id)
    return json_response({'message': 'Event accepted'})


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
        print("Cancelando a aplicação RESTful...\n")
