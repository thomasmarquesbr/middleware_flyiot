import time
import requests
import sys
import json

data_management_service = sys.argv[1]

headers = {
    # 'Authorization' : ‘(some auth code)’,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def verify_availability_service(service):
    try:
        req = requests.get(service['entrypoint'], headers=headers)
        if req.json:
            print("status "+service['type']+": on")
    except requests.ConnectionError:
        print("status "+service['type']+": off")
        try:
            requests.delete(data_management_service+"services/"+service['id'], headers=headers)
        except requests.ConnectionError:
            print("Erro de conexão: "+data_management_service)


def verify_availability_thing(thing):
    try:
        req = requests.get(thing['entrypoint'], headers=headers)
        if req.json:
            print("status "+thing['type']+": on")
    except requests.ConnectionError:
        print("status "+thing['type']+": off")
        # try:
        #     requests.delete(data_management_service+"things/"+thing['id'], headers=headers)
        # except requests.ConnectionError:
        #     print("Erro de conexão: "+data_management_service)


if __name__ == '__main__':
    while True:
        try:
            req = requests.get(data_management_service+"services", headers=headers)
            list_services = json.loads(json.dumps(req.json()))
            req = requests.get(data_management_service+"things", headers=headers)
            list_things = json.loads(json.dumps(req.json()))
            # print(list_services)
            for service in list_services:
                verify_availability_service(service)
            for thing in list_things:
                verify_availability_thing(thing)
        except requests.ConnectionError:
            print("Erro de conexão com o data_management: "+data_management_service)
        time.sleep(10)
        print("-------------------------------------------------------------")
