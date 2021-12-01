import os

import requests


class UserService:
    # endpoint = 'http://host.docker.internal:8001/api/'
    # endpoint = 'http://usersms:8000/api/'
    endpoint = f'{os.getenv("USERS_MS")}/api/'

    @staticmethod
    def get(path, **kwargs):
        headers = kwargs.get('headers', [])
        return requests.get(f'{UserService.endpoint}{path}', headers=headers).json()

    @staticmethod
    def post(path, **kwargs):
        headers = kwargs.get('headers', [])
        data = kwargs.get('data', [])
        return requests.post(f'{UserService.endpoint}{path}', data=data, headers=headers).json()

    @staticmethod
    def put(path, **kwargs):
        headers = kwargs.get('headers', [])
        data = kwargs.get('data', [])
        return requests.put(f'{UserService.endpoint}{path}', data=data, headers=headers).json()
