import os
from pathlib import Path


def notifyEvent(event):
    pass

data_management_service = None
events = {}


class ThingController(object):
    def __init__(self):
        print("Inicializa controller")
        self.__IS_CREATED = False
        self.__IS_MODIFIED = False
        self.__IS_DELETED = False
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
            elif 'isCreated' in observable['condition']:
                self.__IS_CREATED = True
                events[observable['condition']] = observable
            elif 'isModified' in observable['condition']:
                self.__IS_MODIFIED = True
                events[observable['condition']] = observable
            elif 'isDeleted' in observable['condition']:
                self.__IS_DELETED = True
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
            elif key == 'write':
                self.__write(actions['filepath'], value)
            elif key == 'read':
                data = self.__read(value)  # value is filepath
                return data
            elif key == 'filepath':
                pass
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

    def __write(self, filepath, value):
        global data_management_service
        filepath = filepath.replace(":/", "/")
        path = Path(filepath).parent
        if not os.path.exists(path):
            os.makedirs(path)
        mode = 'a' if os.path.exists(filepath) else 'w'
        with open(filepath, mode) as file:
            prefix = ''
            if mode == 'a':
                prefix = '\n'
                if self.__IS_MODIFIED and data_management_service:
                    notifyEvent('isModified')
            else:
                if self.__IS_MODIFIED and data_management_service:
                    notifyEvent('isCreated')
            if self.__STARTS and data_management_service:
                notifyEvent('starts')
            file.write(prefix+value)
            file.close()
            if self.__STOPS and data_management_service:
                notifyEvent('stops')
        return {'message': 'ok'}

    def __read(self, filepath):
        global data_management_service
        filepath = filepath.replace(":/", "/")
        try:
            with open(filepath, 'r') as file:
                content = file.read()
                return {'data': content}
        except EnvironmentError:
            return None

    def set_data_management(self, data_management):
        global data_management_service
        data_management_service = data_management
