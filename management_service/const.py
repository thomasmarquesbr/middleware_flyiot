MIDDLEWARE_NAME = "FlyIoT"
SERVICE_TYPE = "management_service"

DEBUG = False

containers = {
    'discovery': {
        'image': 'thomasmarquesbr/flyiot_discovery:0.2',
        'port': '5000'
    },
    'database': {
        'image': 'mvertes/alpine-mongo',
        'port': '27017'
    },
    'data_management': {
        'image': 'thomasmarquesbr/flyiot_datamanagement:0.2',
        'port': '5001'
    },
    'management': {
        'image': 'thomasmarquesbr/flyiot_management:0.2',
        'port': '5002'
    }
}
