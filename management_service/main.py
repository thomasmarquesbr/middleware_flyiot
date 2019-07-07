import signal
import subprocess
import sys
import uuid


def signal_handling(signum, frame):
    print("Encerrando Management Service ("+ID+")")
    for process in subprocesses:
        process.kill()
    sys.exit()


ID = str(uuid.uuid1())
PORT = str(5002)

subprocesses = [
    subprocess.Popen(["python3.7", "register.py"] + [ID, PORT]),
    subprocess.Popen(["python3.7", "app.py"] + [ID, PORT])
]

signal.signal(signal.SIGINT, signal_handling)
while True:
    subprocesses[0].wait()
