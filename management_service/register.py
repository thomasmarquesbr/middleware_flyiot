from utils import *
from const import *
import sys
from time import sleep
from zeroconf import ServiceInfo, Zeroconf
import signal


def handler(signum, frame):
    finish()


def finish():
    print("Cancelando o registro...\n")
    zeroconf.unregister_service(service_info)
    zeroconf.close()


ID = sys.argv[1]
PORT = sys.argv[2]
ADDRESS = sys.argv[3]
ENTRYPOINT = "/"


data = {
    "id": ID,
    "type": SERVICE_TYPE,
    # "entrypoint": "http://"+ADDRESS+":"+PORT+ENTRYPOINT
    "entrypoint": ("http://localhost:" if DEBUG else "http://"+ADDRESS+":")+PORT+ENTRYPOINT
}

if __name__ == '__main__':
    service_info = ServiceInfo("_http._tcp.local.",
                               ID + "." + MIDDLEWARE_NAME + "._http._tcp.local.",
                               socket.inet_aton(ADDRESS), int(PORT), 0, 0,
                               data, "ash-2.local.")
    zeroconf = Zeroconf()
    print("Registro de um " + SERVICE_TYPE + "(" + ID + ")" + ", press Ctrl-C to exit...")
    signal.signal(signal.SIGABRT, handler)
    zeroconf.register_service(service_info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        finish()
