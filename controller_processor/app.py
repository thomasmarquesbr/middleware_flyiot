import sys
import os
from const import *
from flask import Flask, jsonify, request, make_response, abort
from werkzeug.utils import secure_filename
from controller import ThingController
from utils import get_extension

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
        'cores': '2'
    }
    return make_response(jsonify(info), 200)


@app.route('/actions', methods=['POST'])
def upload_file():
    global thing
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(400)
    if file and get_extension(file.filename) in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # execute_file(filename)
        thing.execute_file(app.config['UPLOAD_FOLDER']+filename)
        return jsonify({'message': 'success'})
    else:
        abort(400)


@app.route('/obervables', methods=['PUT'])
def observe():
    # thing.observe(notify_event())
    return make_response({'message': 'Observable registered'}, 200)


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
