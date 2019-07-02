import subprocess
import uuid

ID = str(uuid.uuid1())
PORT = str(8080)

process1 = subprocess.Popen(["python3.5", "register.py"] + [ID, PORT])
process2 = subprocess.Popen(["python3.5", "app.py"] + [ID, PORT])
process2.wait()
