import logging
import socket
import sys
from discovery_service.const import *
from time import sleep
from typing import cast
import json
import requests

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf


services_discovered = []
list_data_management_service = []
# headers = {"Accept": "application/json"}


def add_resource_to_data_management(info):
    if "service" in info["type"]:
        print("Service encontrado:")
        if "data_management" in info["type"]:
            list_data_management_service.append(info["entrypoint"])

        if len(list_data_management_service) > 0:
            data = json.dumps(info)
            # print(data)
            req = requests.post(list_data_management_service[0]+"services", json=data)
            print(req.json())
    else:
        print("Thing encontrado:")
        # req = requests.delete("https://jsonplaceholder.typicode.com/todos/1")
    print(json.dumps(info, indent=2))


def remove_service_to_data_management(info):
    if "service" in info.type["type"]:
        print("Removendo service:  > ")

    else:
        print("Removendo Thing:")


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
            service_info = zeroconf.get_service_info(service_type, name)
            if service_info:
                services_discovered.remove(name)

        print('\n\n')


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
        zeroconf.close()

