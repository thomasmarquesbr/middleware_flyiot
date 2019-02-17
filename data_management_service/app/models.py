import operator
import re
from enum import Enum

from utils import is_valid_ip



class Service_Type(Enum):
    DISCOVERY = 1
    MANAGEMENT = 2
    DATA_MANAGEMENT = 3


class Service(object):
    def __init__(self, id, name, serviceType, ip):
        self.id = id
        self.name = name
        self.service_type = serviceType
        self.ip = ip
    
    id = property(operator.attrgetter('_id'))
    name = property(operator.attrgetter('_name'))
    service_type = property(operator.attrgetter('_service_type'))
    ip = property(operator.attrgetter('_ip'))

    @id.setter
    def id(self, i):
        if not i: raise Exception("id não deve ser nulo")
        self._id = i

    @name.setter
    def name(self, n):
        if not n: raise Exception("nome não deve ser nulo")
        self._name = n

    @service_type.setter
    def service_type(self, t):
        if not isinstance(t, Service_Type): raise Exception("Service_type inválido")
        self._service_type = t.name

    @ip.setter
    def ip(self, i):
        if not is_valid_ip(i):
            raise Exception("ip Inválido")
        self._ip = i

