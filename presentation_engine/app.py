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
events = {}

app = Flask(__name__)
if DEBUG:
    app.debug = True


def subscribe_events():
    global parser
    global type_things_discovered
    global data_management_service
    global workflows
    global events

    things = parser.things
    workflows = parser.workflows
    group_events = []
    for name, workflow in workflows.copy().items():
        # print('name: '+name)
        for i, item in enumerate(workflow['when']):
            # print(str(i)+' '+str(item))
            for key, value in item.copy().items():
                event_id = str(uuid.uuid1()) + '_' + name + '_' + 'when' + '_' + str(i) + '_' + key
                workflows[name]['when'][i]['status'] = False
                # group_events[event_id] = value
                if key in things.keys():
                    event = {
                        'id': event_id,
                        'condition': value,
                        'thing': things[key]['type']
                    }
                    group_events.append(event)
                    event['status'] = False
                    events[event_id] = event
                else:
                    event = {
                        'id': event_id,
                        'condition': value,
                        'workflow': key
                    }
                    group_events.append(event)
                    event['status'] = False
                    events[event_id] = event

    if len(group_events) > 0:
        try:
            req = requests.put(data_management_service + 'events', json=group_events, headers=headers)
            print(req.json())
        except requests.ConnectionError:
            print("Erro de conexão: " + data_management_service + "events")
    # print(json.dumps(group_events, indent=2))


if filepath:
    parser = FlyIoTLParser(filepath)
    parser.syntax_validate()
    parser.semantic_validate()


def get_types_discovered():
    try:
        req = requests.get(data_management_service + 'types', headers=headers)
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
        return make_response(jsonify({'message': 'data_management added successfuly'}), 200)
    else:
        abort(400)


@app.route('/notification/<event_id>', methods=['PUT', 'POST'])
def notification(event_id):
    global parser
    global workflows
    global events

    things = parser.things
    id = event_id.split('_')
    # print(id)
    workflows[id[1]][id[2]][int(id[3])]['status'] = True
    check_workflow(workflows[id[1]])
    check_another_workflows(id[1])
    print(json.dumps(workflows, indent=2))
    clear_workflow(workflows[id[1]])
    return make_response(jsonify({'message': 'Event accepted'}), 200)


def clear_workflow(workflow):
    status = True
    for event in workflow['when']:
        if 'status' in event.keys() and event['status'] is not True:
            status = False
    if status:
        for event in workflow['when']:
            event['status'] = False


def check_workflow(workflow):
    # print(json.dumps(workflow, indent=1))
    status = True
    for event in workflow['when']:
        if 'status' in event.keys() and event['status'] is not True:
            status = False
    if status:
        trigger_actions(workflow['do'])
    # print(json.dumps(workflow, indent=2))
    # for event in workflow['when']:
    #     event['status'] = False


def check_another_workflows(event_name):
    global workflows
    # print(workflows)
    for key, workflow in workflows.items():
        if event_name != key:  # Nao é o proprio workflow
            when_events = workflow['when']
            for i in range(len(when_events)):
                if event_name in when_events[i].keys() and when_events[i][event_name] == 'starts':
                    workflows[key]['when'][i]['status'] = True
                    # trigger_actions(workflow['do'])

            check_workflow(workflow)


def trigger_actions(actions_workflow):
    global data_management_service
    global parser
    things = parser.things
    # print(things)
    for action in actions_workflow:
        my_thing = next(iter(action))
        # print(things[my_thing]['type'])
        try:
            print('action-> '+str(action))
            req = requests.put(data_management_service+'actions/'+my_thing, json=action, headers=headers)
            print(req.json())
        except requests.ConnectionError:
            print('Erro ao conectar em: '+data_management_service+'actions/'+my_thing)


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
