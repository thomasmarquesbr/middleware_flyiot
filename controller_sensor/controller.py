import asyncio


class ThingController(object):
    def __init__(self):
        print("Inicializa controller")
    #     Configurar Controller

    async def observe(self, observables):
        print("Observe element")
        await asyncio.sleep(0.01)
        for observable, value in observables:
            if observable is 'measurement':
                self.__start_observe_measurement(value)
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
            elif key == 'turn':
                self.__turn(value)
            elif key == 'measurement':
                self.__measurement(value)
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

    def __turn(self, value):
        print("action -> turn: "+str(value))
        return {'message': 'ok'}

    def __measurement(self, value):
        print('action -> measurement: '+str(value))
        return {'measurement': 25}

    def __start_observe_measurement(self, value):
        pass
