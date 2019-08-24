import asyncio
from utils import map_to_GPIOColor
import RPi.GPIO as GPIO
import requests
from const import *

data_managament_service = None
events = {}
            

def notify_event(event):
    global events
    global data_management_service
    print('notify_event')
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
        self.__PRESSED = False
        self.__setup_GPIO()
        
    def __del__(self):
        GPIO.cleanup()
        
    def __setup_GPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.__GPIO_PIN = 17
        GPIO.setup(self.__GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.__GPIO_PIN, GPIO.FALLING, callback=self.push_button_detected, bouncetime=100)
        
    def push_button_detected(self, null):
        global events
        global data_management_service
        print("Signal detected")
        if self.__STARTS and data_management_service:
            notify_event('starts')
        if self.__STARTS and data_management_service:
            notify_event('pressed')
#             try:
#                 if event in events.keys():
#                     req = requests.put(data_management_service+'events/'+str(events[event]['id']), headers=headers)
#                     print(req.json)
#                     del events[event]
#             except requests.ConnectionError:
#                 print('Erro de conexao')        
    
#     def observe(self, entrypoint, observables):
#         global data_management_service
#         data_management_service = entrypoint
#         for key, observe in observables.items():
#             if observe == 'pressed' or observe == 'starts':
#                 global uuid
#                 global value
#                 uuid = key
#                 value = observe
#                 GPIO.add_event_detect(self.__GPIO_PIN, GPIO.FALLING, callback=push_button_detected, bouncetime=100)
                
    def observe(self, observable):
        print('Observe element:')
        print(observable)
        if 'condition' in observable.keys():
            if 'starts' in observable['condition']:
                self.__STARTS = True
                events[observable['condition']] = observable
            elif 'pauses' in observable['condition']:
                self.__PAUSES = True
                events[observable['condition']] = observable
            elif 'resumes' in observable['condition']:
                self.__RESUMES = True
                events[observable['condition']] = observable
            elif 'stops' in observable['condition']:
                self.__STOPS = True
                events[observable['condition']] = observable
            elif 'pressed' in observable['condition']:
                self.__PRESSED = True
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
    
    def set_data_management(self, data_management):
        global data_management_service
        data_management_service = data_management


