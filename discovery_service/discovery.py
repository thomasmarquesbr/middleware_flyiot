from const import *
from utils import *
import json
import logging
import sys
import requests
from time import sleep
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

services_discovered = []
list_data_management_service = []
list_management_service = []
headers = {
    # 'Authorization' : ‘(some auth code)’,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def add_resource_to_data_management(info):
    global list_data_management_service
    if "service" in info["type"]:
        print("Service encontrado:")
        if "data_management" in info["type"]:
            list_data_management_service.append(info)
        elif "management_service" in info["type"]:
            list_management_service.append(info["entrypoint"])
            if info["entrypoint"] and len(list_data_management_service) > 0:
                try:
                    req = requests.post(info["entrypoint"]+"data_management", json=list_data_management_service[0], headers=headers)
                    print(req.json())
                except requests.ConnectionError:
                    print("Erro de conexão: "+info["entrypoint"]+"data_management")
        elif "discovery_service" in info["type"]:
            print("Discovery Service encontrado")

        if len(list_data_management_service) > 0:
            for data_management in list_data_management_service:
                try:
                    req = requests.post(data_management["entrypoint"]+"services", json=info, headers=headers)
                    print(req.json())
                except requests.ConnectionError:
                    print("Erro de conexão: "+data_management["entrypoint"]+"services")

    else:
        print("Thing encontrado:")
        if info["entrypoint"] and len(list_data_management_service) > 0:
            add_new_thing_discovered(list_data_management_service[0], info)
    print(json.dumps(info, indent=2))


def add_new_thing_discovered(data_management, thing):
    try:
        req = requests.post(data_management['entrypoint']+"things", json=thing, headers=headers)
        print(req.json)
    except requests.ConnectionError:
        print("Erro de conexão: " + data_management + "things")


def on_service_state_change(zeroconf: Zeroconf,
                            service_type: str,
                            name: str,
                            state_change: ServiceStateChange) -> None:
    if MIDDLEWARE_NAME in name:
        print("---------------------------------------")
        # print("Service %s do tipo %s foi %s" % (name, service_type, state_change))

        if state_change is ServiceStateChange.Added:
            service_info = zeroconf.get_service_info(service_type, name)
            if service_info and service_info.properties:
                services_discovered.append(name)
                properties = {}
                for key, value in service_info.properties.items():
                    properties[key.decode("utf-8")] = value.decode("utf-8")
                add_resource_to_data_management(properties)
            else:
                print("  No info")

        elif state_change is ServiceStateChange.Removed:
            print("Removed")

        print('\n')
        # print(services_discovered)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    print("\nBrowsing services, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Cancelando o discovery...\n")
        zeroconf.close()
