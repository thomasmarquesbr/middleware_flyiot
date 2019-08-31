from const import *
import signal
import subprocess
import sys
import uuid
import random
from utils import get_address_ip


def signal_handling(signum, frame):
    print("Encerrando Management Service ("+ID+")")
    for process in subprocesses:
        process.kill()
    sys.exit()


ID = str(uuid.uuid1())
PORT = str(5002)# if DEBUG else random.randint(49152, 65535))
ADDRESS = sys.argv[1] if len(sys.argv) > 1 else get_address_ip()

subprocesses = [
    subprocess.Popen(["python3.7", "register.py"] + [ID, PORT, ADDRESS]),
    subprocess.Popen(["python3.7", "app.py"] + [ID, PORT])
]

signal.signal(signal.SIGINT, signal_handling)
while True:
    subprocesses[0].wait()
