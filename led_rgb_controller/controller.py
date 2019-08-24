import asyncio
from utils import map_to_GPIOColor
import RPi.GPIO as GPIO


data_managament_service = None
events = {}


def notify_event(event):
    global events
    global data_management_service
    try:
        if event in events.keys():
            req = requests.put(data_management_service+'events/'+str(events[event]['id']), headers=headers)
            print(req.json)
            del events[event]
    except requests.ConnectionError:
        print('Erro de conexao')


class ThingController(object):
    def __init__(self):
        print("Inicializa controller")
        self.__STARTS = False
        self.__RESUMES = False
        self.__STOPS = False
        self.__PAUSES = False
        self.__setup_GPIO()
        
    def __del__(self):
        GPIO.cleanup()
        
    def __setup_GPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        red = 3
        green = 4
        blue = 2
        TIME = 1
        GPIO.cleanup()
        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(blue, GPIO.OUT)
        freq = 100
        self.__RED = GPIO.PWM(red, freq)
        self.__GREEN = GPIO.PWM(green, freq)
        self.__BLUE = GPIO.PWM(blue, freq)
        self.__RED.start(0)
        self.__GREEN.start(0)
        self.__BLUE.start(0)
        
    def observe(self, observable):
        print('Observe element:')
        print(observable)
        if 'condition' in observable.keys():
            if 'starts' in observable['condition']:
                self.__STARTS = True
                events[observable['condition']] = observable
            elif 'starts' in observable['condition']:
                self.__STARTS = True
                events[observable['condition']] = observable
            elif 'starts' in observable['condition']:
                self.__STARTS = True
                events[observable['condition']] = observable
            elif 'starts' in observable['condition']:
                self.__STARTS = True
                events[observable['condition']] = observable
            else:
                return False
        return True
        

    def actions(self, actions):
        for key, value in actions.items():
            if key == 'action': 
                if value == 'start':
                    self.__start()              
                elif value == 'stop':
                    self.__stop()
                elif value == 'pause':
                    self.__pause()
                elif value == 'resume':
                    self.__resume()
                else:
                    return None
            elif key == 'setColor':
                self.__set_color(value)
            else:
                return None
        return {'message': 'ok'}

    def __start(self):
        print('action -> start')
        if self.__STARTS and data_management_service:
            notify_event('starts')
        self.__RED.start(100)
        self.__GREEN.start(100)
        self.__BLUE.start(100)
        return {'message': 'ok'}

    def __stop(self):
        print('action -> stop')
        if self.__STOPS and data_management_service:
            notify_event('stops')
        self.__RED.start(0)
        self.__GREEN.start(0)
        self.__BLUE.start(0)
        return {'message': 'ok'}

    def __pause(self):
        print('action -> pause')
        if self.__PAUSES and data_management_service:
            notify_event('pauses')
        self.__RED.start(100)
        self.__GREEN.start(100)
        self.__BLUE.start(100)
        return {'message': 'ok'}

    def __resume(self):
        print('action -> resume')
        if self.__RESUMES and data_management_service:
            notify_event('resumes')
        self.__RED.start(0)
        self.__GREEN.start(0)
        self.__BLUE.start(0)
        return {'message': 'ok'}

    def __set_color(self, value):
        print("action -> turn: "+str(value))
        colors = map_to_GPIOColor(str(value))
        if len(colors) == 3:
            self.__RED.start(colors[0])
            self.__GREEN.start(colors[1])
            self.__BLUE.start(colors[2])
        return {'message': 'ok'}
    
    def set_data_management(self, data_management):
        global data_management_service
        data_management_service = data_management

