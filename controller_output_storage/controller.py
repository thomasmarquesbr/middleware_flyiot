import os
from pathlib import Path


def notifyEvent(event):
    pass


class ThingController(object):
    def __init__(self):
        print("Inicializa controller")
        self.__IS_CREATED = False
        self.__IS_MODIFIED = False
        self.__IS_DELETED = False
        self.__STARTS = False
        self.__STOPS = False
        self.__PAUSES = False
        self.__RESUMES = False
    #     Configurar Controller

    # async def observe(self, observables):
    #     print("Observe element")
    #     await asyncio.sleep(0.01)
    #     for observable, value in observables:
    #         if observable is 'measurement':
    #             self.__start_observe_measurement(value)
    #         else:
    #             return False
    #     return True

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
                data = self.__read()
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
        filepath = filepath.replace(":/", "/")
        path = Path(filepath).parent
        if not os.path.exists(path):
            os.makedirs(path)
        mode = 'a' if os.path.exists(filepath) else 'w'
        with open(filepath, mode) as file:
            prefix = ''
            if mode == 'a':
                prefix = '\n'
                if self.__IS_MODIFIED:
                    notifyEvent('isModified')
            else:
                if self.__IS_MODIFIED:
                    notifyEvent('isCreated')
            file.write(prefix+value)
            file.close()
            notifyEvent('starts')
        return {'message': 'ok'}

    def __read(self):
        print('read -> read:')
        return 'measurement'

    def __start_observe_measurement(self, value):
        pass
