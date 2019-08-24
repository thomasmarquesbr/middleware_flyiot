import signal
import subprocess
import sys
import uuid
import random
from const import *


def signal_handling(signum, frame):
    print("Encerrando Thing ("+ID+")")
    for process in subprocesses:
        process.kill()
    sys.exit()


ID = str(uuid.uuid1())
# PORT = str(6000 if DEBUG else random.randint(49152, 65535))
PORT = str(6001)

subprocesses = [
    subprocess.Popen(["python3.7", "register.py"] + [ID, PORT]),
    subprocess.Popen(["python3.7", "app.py"] + [ID, PORT]),
]

signal.signal(signal.SIGINT, signal_handling)
while True:
    subprocesses[0].wait()
