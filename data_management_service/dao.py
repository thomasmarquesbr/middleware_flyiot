class ThingsDao(object):

    def __init__(self):
        # self.__db = db
        self.__resources = []
        self.__devices = []

    # Resources
    def add_resource(self, resource):
        self.__resources.append(resource)

    def remove_resource(self, resource):
        self.__resources.remove(resource)

    def list_resources(self):
        return self.__resources

    def get_resource(self, res):
        return self.__resources[res]

    # Devices
    def add_device(self, device):
        self.__devices.append(device)

    def remove_device(self, device):
        self.__devices.remove(device)

    def list_devices(self):
        return self.__devices


class ServicesDao(object):

    def __init__(self):
        self.__services = []

    def add_services(self, service):
        self.__services.append(service)

    def remove_resource(self, service):
        self.__services.remove(service)

    def list_services(self):
        return self.__services
