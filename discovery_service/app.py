import sys
from const import *
from flask import Flask, jsonify


ID = sys.argv[1]
PORT = sys.argv[2]

print("Iniciando Discovery Service")

app = Flask(__name__)
if DEBUG:
    app.debug = True


@app.route('/')
def get_hello():
    return jsonify({'message': 'Hello World'})


if __name__ == '__main__':
    try:
        if DEBUG:
            app.run(port=int(PORT))
        else:
            app.run(host='0.0.0.0', port=int(PORT))
    except KeyboardInterrupt:
        pass
    finally:
        print("Cancelando a aplicação RESTful...\n")


