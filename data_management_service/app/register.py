from data_management_service.app.utils import *
from data_management_service.app.const import *
import sys
from time import sleep
from zeroconf import ServiceInfo, Zeroconf


ID = sys.argv[1]
ADDRESS = get_address_ip()
PORT = sys.argv[2]
ENTRYPOINT = "/"

data = {
    "id": ID,
    "type": SERVICE_TYPE,
    # "entrypoint": "http://"+ADDRESS+":"+PORT+ENTRYPOINT
    "entrypoint": "http://localhost:"+PORT+ENTRYPOINT
}

if __name__ == '__main__':
    service_info = ServiceInfo("_http._tcp.local.",
                               ID + "." + MIDDLEWARE_NAME + "._http._tcp.local.",
                               socket.inet_aton(ADDRESS), 5001, 0, 0,
                               data, "ash-2.local.")
    zeroconf = Zeroconf()
    print("Registro de um " + SERVICE_TYPE + "(" + ID + ")" + ", press Ctrl-C to exit...")
    zeroconf.register_service(service_info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Cancelando o registro...")
        zeroconf.unregister_service(service_info)
        zeroconf.close()
