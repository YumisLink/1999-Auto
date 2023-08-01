import requests
import json
from hashlib import md5
from enum import Enum

url = 'http://localhost:8000'

def set_server(new_url: str):
    global url
    url = new_url

def login(username: str, password: str) -> str:
    password = md5((password+username).encode()).hexdigest()
    response = requests.post(url + '/login', data={'username': username, 'password': password})
    res = response.json()
    if 'success' not in res or not res['success']:
        raise Exception(res['detail'])
    return response.cookies['access-token']

def get_tasks(token: str) -> list:
    response = requests.get(url + '/get_tasks', cookies={'access-token': token})
    res = response.json()
    if 'success' not in res or not res['success']:
        raise Exception(res['detail'])
    return res['tasks']

def get_task(token: str, task_id: int) -> dict:
    response = requests.get(url + '/get_task', params={'task_id': task_id}, cookies={'access-token': token})
    res = response.json()
    if 'success' not in res or not res['success']:
        raise Exception(res['detail'])
    return res['task']

def set_energy(token: str, task_id: int, energy: int):
    response = requests.get(url + '/set_energy', params={'task_id': task_id, 'energy': energy}, cookies={'access-token': token})
    res = response.json()
    if 'success' not in res or not res['success']:
        raise Exception(res['detail'])
    return

class LogLevel(Enum):
    DEBUG = 0
    HERTBEAT = 1
    INFO = 2
    NOTICE = 3
    WARNING = 4
    ERROR = 5

def log(token: str, task_id: int, level: LogLevel, message: str):
    # print(f"LOG {level.name}: {message}")
    response = requests.post(url + '/log', params={'task_id': task_id, 'level': level.value}, json={'message': message}, cookies={'access-token': token})
    res = response.json()
    if 'success' not in res or not res['success']:
        raise Exception(res['detail'])
    return

def email(token: str, task_id: int, title: str, content: str):
    # print(f"EMAIL {title}: {content}")
    response = requests.post(url + '/email', params={'task_id': task_id}, json={'title': title, 'content': content}, cookies={'access-token': token})
    res = response.json()
    if 'success' not in res or not res['success']:
        raise Exception(res['detail'])
    return