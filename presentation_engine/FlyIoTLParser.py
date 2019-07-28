import yaml
import re
from cerberus import *


events = ['starts', 'stops', 'pauses', 'resumes']
actions = ['start', 'stop', 'pause', 'resume', 'write', 'read']

schema_thing = {
    'thing': {
        'type': 'string',
        'required': True
    },
    'type': {
        'type': 'string',
        'required': True
    },
    'addr': {'type': 'string'},
    'params': {'type': 'list'},
    'requirements': {'type': 'dict'},
    'filepath': {'type': 'string'},
    'lang': {'type': ['string', 'list']},
    'code': {
        'type': 'string',
        'excludes': 'sourcepath'
    },
    'sourcepath': {
        'type': 'string',
        'excludes': 'code'
    }
}

schema_workflow = {
    'workflow': {
        'type': 'string',
        'required': True
    },
    'when': {
        'required': True,
        'type': 'list',
        'empty': False,
        'schema': {
            'type': 'dict',
            'allow_unknown': True
        }
    },
    'do': {
        'required': True,
        'type': 'list',
        'empty': False,
        'schema': {
            'type': 'dict',
            'allow_unknown': True,
            'schema': {
                'reference': {'type': 'string'}
            }
        }
    }
}

schema_FlyIoTL = {
    'FlyIoTL': {
        'required': True,
        'schema': {
            'things': {
                'required': True,
                'type': 'list',
                'empty': False,
                'schema': {
                    'type': 'dict',
                    'schema': schema_thing
                }
            },
            'workflows': {
                'required': True,
                'type': 'list',
                'empty': False,
                'schema': {
                    'type': 'dict',
                    'schema': schema_workflow
                }
            }
        }
    }
}


class FlyIoTLParser(object):
    def __init__(self, path):
        # schema = eval(open('schema_FlyIoTL.py', 'r').read())
        self.__syntax_validator = Validator(schema_FlyIoTL)
        self.__doc = self.__load_file(path)
        self.things = {}
        self.workflows = {}

    @staticmethod
    def __load_file(path):
        with open(path, 'r') as stream:
            try:
                return yaml.load(stream, Loader=yaml.Loader)
            except yaml.YAMLError as exception:
                raise exception

    def syntax_validate(self):
        if not self.__syntax_validator.validate(self.__doc, schema_FlyIoTL):
            raise Exception(self.__syntax_validator.errors)

    def semantic_validate(self):

        for thing in self.__doc['FlyIoTL']['things']:
            if thing['thing'] in self.things.keys():
                msg = '{} already definite in "FlyIoT.Things"'.format(thing['thing'])
                raise Exception(msg)
            # things_name.append(thing['thing'])
            self.things[thing['thing']] = thing

        for workflow in self.__doc['FlyIoTL']['workflows']:
            if workflow['workflow'] in self.workflows.keys():
                msg = '{} already definite in "FlyIoT.Workflows"'.format(workflow['workflow'])
                raise Exception(msg)
            self.workflows[workflow['workflow']] = workflow

        for workflow in self.__doc['FlyIoTL']['workflows']:
            for event in workflow['when']:

                # Event validator
                for key, value in event.items():
                    if key not in self.things.keys() and key not in self.workflows.keys():
                        msg = '"{}" not defined in "FlyIoTL.Things" or "FlyIoTL.Workflows"'.format(key)
                        raise Exception(msg)

                    # validar eventos padrão (gesture, evento especifico), expressão ou intervalo
                    if key in self.things.keys():
                        if value in ['starts', 'stops', 'resumes', 'pauses']:
                            pass
                        elif re.compile('\[\d+[.,]?\d*-\d+[.,]?\d*\]').match(value) or \
                                re.compile('(>|<|>=|<=|=)\d+[\w!@#$%&-_+=]+').match(value):
                            pass
                        elif 'requirements' in self.things[key].keys() and \
                                'events' in self.things[key]['requirements'].keys() and \
                                value in self.things[key]['requirements']['events']:
                            pass
                        elif 'requirements' in self.things[key].keys() and \
                                'gestures' in self.things[key]['requirements'].keys() and \
                                value in self.things[key]['requirements']['gestures']:
                            pass
                        else:
                            msg = '"{}" is not default event or not defined in requirements from "FlyIoT.things.{}"'.format(value, key)
                            raise Exception(msg)

            for action in workflow['do']:

                # Action validator
                last_thing = None
                for key, value in action.items():
                    if key in self.things.keys():  # nome do thing
                        last_thing = key
                        if value in actions:
                            pass
                        elif 'storage' in str(self.things[last_thing]['type']).lower() and value in ['write', 'read']:
                            pass
                        else:
                            msg = '{} is not default event (start, stop, pause, resume, write, read)'.format(value)
                            raise Exception(msg)
                    elif key == 'reference':
                        pass
                    elif key in self.things[last_thing]['params']:  # parametro mandatório
                        pass
                    elif str(key+'?') in self.things[last_thing]['params']:  # parametro opcional
                        pass
                    else:
                        msg = '{} not defined in "FlyIoTL.Things.{}, is not "reference" field, is not optional or ' \
                              'mandatory param'.format(key, last_thing)
                        raise Exception(msg)
