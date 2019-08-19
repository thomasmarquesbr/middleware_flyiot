import subprocess
import sys
import signal


def signal_handling(signum, frame):
    print("signal_handling")
    # for process in subprocesses:
    #     process.kill()
    # sys.exit()


sub = subprocess.Popen(["python3.7", "teste2.py"])
# stdout, stderr = sub.communicate()
print("alsejalskj")
print("Alse")
print("aselkjalse")


# print(stdout)
# print(stderr)
signal.signal(signal.SIGCHLD, signal_handling)


while True:
    sub.wait()
