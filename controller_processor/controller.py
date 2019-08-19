import asyncio
import subprocess
import signal
from utils import get_extension, extract_file


def signal_handling(self, signum, frame):
    print("signal_handling")


class ThingController(object):
    def __init__(self):
        print("Inicializa controller")
        self.__STARTS = False
        self.__STOPS = False
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
        extension = get_extension(filename)
        if extension == 'py':
            sub = subprocess.Popen(["python3.7", filename])
            stdout = sub.communicate()
            if self.__STOPS:
                print("teste")
            # signal.signal(signal.SIGCHLD, signal_handling)
        elif extension == 'gz' or extension == 'tar':
            extract_file(filename)


