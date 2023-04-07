import os
from multiprocessing import Process
import time

import requests
from pytest import fixture

@fixture(scope='session')
def start_api():

    def start():
        from backend.main import Service
        service = Service(True)
        service.start()

    process = Process(target=start)
    process.start()
    time.sleep(1)
    yield 1
    process.terminate()
    os.remove('database_test.sqlite')

@fixture()
def access_token() -> str:
    response = requests.post(
        'http://localhost:5000/user/login',
        json={
            'username': 'admin',
            'password': 'admin'
        }
    ).json()
    header = {
        'Authorization': f'Bearer {response["access_token"]}'
    }
    return header