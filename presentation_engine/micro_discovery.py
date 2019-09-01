import logging
import sys
import json
import requests
from const import *
from time import sleep
from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf


RUNNING = True
list_services = []
list_processors = []


def send_file_to_start_data_management_service():
    global RUNNING
    processor = list_processors[0]
    try:
        files = {'file': open('start_management_service.py', 'rb')}
        req = requests.post(processor['entrypoint']+'actions', files=files)
        print(req.json())
        RUNNING = False
    except requests.ConnectionError:
        print('Erro ao conextar em '+processor['entrypoint']+'actions')


def check_processors():
    services_types = []
    for service in list_services:
        services_types.append(service['type'])
    if len(list_processors) > 0 and 'management_service' not in services_types:
        send_file_to_start_data_management_service()


def save_new_resource_discovered(info):
    global list_services
    if "service" in info["type"]:
        print("Service encontrado:")
        list_services.append(info)
    elif "processor" in info['type']:
        print("Processor encontrado:")
        list_processors.append(info)
    print(json.dumps(info, indent=2))


def on_service_state_change(zeroconf: Zeroconf,
                            service_type: str,
                            name: str,
                            state_change: ServiceStateChange) -> None:
    if MIDDLEWARE_NAME in name:
        print("---------------------------------------")
        if state_change is ServiceStateChange.Added:
            service_info = zeroconf.get_service_info(service_type, name)
            if service_info and service_info.properties:
                # services_discovered.append(name)
                properties = {}
                for key, value in service_info.properties.items():
                    properties[key.decode("utf-8")] = value.decode("utf-8")
                save_new_resource_discovered(properties)
            else:
                print("  No info")
        elif state_change is ServiceStateChange.Removed:
            print("Removed")
        print('\n')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    print("\nBrowsing services, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])
    try:
        while RUNNING:
            sleep(5)
            check_processors()
    except KeyboardInterrupt:
        pass
    finally:
        print("Cancelando o discovery...\n")
        zeroconf.close()