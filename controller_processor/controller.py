import asyncio
import subprocess
import signal
import requests
from const import headers
from util import get_extension, extract_file
import os


def signal_handling(self, signum, frame):
    print("signal_handling")


data_management_service = None
events = {}


def notify_event(event):
    global events
    global data_management_service
    try:
        if event in events.keys():
            # print(data_management_service+'events/'+events[event]['id'])
            req = requests.put(data_management_service+'events/'+str(events[event]['id']), headers=headers)
            print(req.json)
            del events[event]
    except requests.ConnectionError:
        print('Erro de conexão ')


class ThingController(object):
    def __init__(self):
        print("Inicializa controller")
        self.__STARTS = False
        self.__STOPS = False
    #     Configurar Controller

    def observe(self, observable):
        print("Observe element:")
        print(observable)
        if 'condition' in observable.keys():
            if 'starts' in observable['condition']:
                self.__STARTS = True
                events[observable['condition']] = observable
            elif 'stops' in observable['condition']:
                self.__STOPS = True
                events[observable['condition']] = observable
            else:
                return False
        return True

    def actions(self, actions):
        for key, value in actions.items():
            if key == 'start':
                self.__start()
            elif key == 'stop':
                self.__stop()
            elif key == 'pause':
                self.__pause()
            elif key == 'resume':
                self.__resume()
            else:
                return None
        return {'message': 'ok'}

    def __start(self):
        print('action -> start')
        return {'message': 'ok'}

    def __stop(self):
        print('action -> stop')
        return {'message': 'ok'}

    def __pause(self):
        print('action -> pause')
        return {'message': 'ok'}

    def __resume(self):
        print('action -> resume')
        return {'message': 'ok'}

    def execute_file(self, filename):
        global data_management_service
        extension = get_extension(filename)
        if extension == 'py':
            sub = subprocess.Popen(["python3.7", filename])
            if self.__STARTS and data_management_service:
                notify_event('starts')
            stdout = sub.communicate()
            if self.__STOPS and data_management_service:
                notify_event('stops')
            os.remove(filename)
        elif extension == 'gz' or extension == 'tar':
            extract_file(filename)

    def set_data_management(self, data_management):
        global data_management_service
        data_management_service = data_management


