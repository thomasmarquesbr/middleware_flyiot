from const import *
import subprocess
import uuid
import sys
import signal
import random


def signal_handling(signum, frame):
    print("Encerrando Data Management Service ("+ID+")")
    for process in subprocesses:
        process.kill()
    sys.exit()


ID = str(uuid.uuid1())
PORT = str(5001)# if DEBUG else random.randint(49152, 65535))

subprocesses = [
    subprocess.Popen(["python3.7", "register.py"] + [ID, PORT]),
    subprocess.Popen(["python3.7", "app.py"] + [ID, PORT])
]

signal.signal(signal.SIGINT, signal_handling)
while True:
    subprocesses[0].wait()
