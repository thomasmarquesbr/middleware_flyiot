import sys
from util import get_address_ip
from const import *
import socket
from time import sleep
from zeroconf import ServiceInfo, Zeroconf


ID = sys.argv[1]
ADDRESS = get_address_ip()
PORT = sys.argv[2]
ENTRYPOINT = "/"

data = {
    "id": ID,
    "type": THING_TYPE,
    # "entrypoint": "http://"+ADDRESS+":"+PORT+ENTRYPOINT
    "entrypoint": ("http://localhost:" if DEBUG else "http://"+ADDRESS+":")+PORT+ENTRYPOINT
}

if __name__ == '__main__':
    service_info = ServiceInfo("_http._tcp.local.",
                               ID + "." + MIDDLEWARE_NAME + "._http._tcp.local.",
                               socket.inet_aton(ADDRESS), int(PORT), 0, 0,
                               data, "ash-2.local.")
    zeroconf = Zeroconf()
    print("Registro de um " + THING_TYPE + "(" + ID + ")" + ", press Ctrl-C to exit...")
    zeroconf.register_service(service_info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Cancelando o registro...\n")
        zeroconf.unregister_service(service_info)
        zeroconf.close()
