import sys
import os
from const import *
from flask import Flask, jsonify, request, make_response, abort
from controller import ThingController
from werkzeug.utils import secure_filename
from util import get_extension

ID = sys.argv[1]
PORT = sys.argv[2]

print("Iniciando Controller Processor")

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'py', 'gz', 'tar'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if DEBUG:
    app.debug = True


thing = ThingController()


@app.route('/')
def get_hello():
    info = {
        'language': ['Python3', 'Python2'],
        'cores': '2',
        'support': 'Docker-container'
    }
    return make_response(jsonify(info), 200)


@app.route('/data_management', methods=['POST'])
def add_data_management():
    info = request.json
    if 'entrypoint' in info:
        data_management = info['entrypoint']
        thing.set_data_management(data_management)
    return make_response(jsonify({'message': 'data_management added'}), 200)


@app.route('/actions', methods=['POST'])
def upload_file():
    global thing
    if 'file' not in request.files:
        print('acá1')
        abort(400)
    file = request.files['file']
    print(file)
    if file.filename == '':
        print('aca2')
        abort(400)
    if file and get_extension(file.filename) in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        thing.execute_file(app.config['UPLOAD_FOLDER']+filename)
        return jsonify({'message': 'success'})
    else:
        print('aca3')
        abort(400)


@app.route('/observables', methods=['PUT', 'POST'])
def observe():
    global thing
    json = request.json
    thing.observe(json)
    return make_response(jsonify({'message': 'Observable registered'}), 200)


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
