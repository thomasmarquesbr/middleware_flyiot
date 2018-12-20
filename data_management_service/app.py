from flask import Flask
from flask_pymongo import PyMongo
from data_management_service.dao import ThingsDao, ServicesDao
import json

app = Flask(__name__)

thingsDao = ThingsDao()
servicesDao = ServicesDao()
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)


@app.route('/hello')
def get_services():
    return json.dumps(["Hello World"])


@app.route('/devices')
def get_devices():
    return json.dumps(thingsDao.list_devices())


@app.route('/resources')
def get_resources():
    return json.dumps(thingsDao.list_resources())


@app.route('/resource/<item>')
def get_resource(item):
    resource = ThingsDao.get_resource(item)
    if resource is not None:
        return json.dumps(thingsDao)
    else:
        return json.dumps([])


if __name__ == '__main__':
    thingsDao.add_device({"id": "id1"})
    thingsDao.add_device({"id": "id2"})
    app.run(port=8080)
