from flask import Flask
from discovery_service import discovery
import os


os.system("python3 register.py &")
os.system("python3 discovery.py &")
app = Flask(__name__)


@app.route('/services')
def get_services():
    return discovery.services_on


if __name__ == '__main__':
    app.run()


# import os


