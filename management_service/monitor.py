import time
import requests
import sys
import json

data_management_service = sys.argv[1]

headers = {
    # 'Authorization' : ‘(some auth code)’,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

if __name__ == '__main__':
    while True:
        req = requests.get(data_management_service+"services", headers=headers)
        print(json.dumps(req.json(), indent=2))
        time.sleep(10)
