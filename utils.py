import os
import signal
import subprocess
import time

from requests.auth import HTTPBasicAuth
import requests
from requests.exceptions import ConnectionError
from constants import REST_API_URL, USERNAME, PASSWORD, ENDPOINT_PORT




def send_request():
    try:
        basic = HTTPBasicAuth(USERNAME, PASSWORD)
        response = requests.get(REST_API_URL.format(1), auth=basic)
        if response.status_code == 200:
            print("Request successful")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except ConnectionError as e:
        print(f"Failed to send request due to connection error exception")
        raise e
    except Exception as e:
        print(f"Request failed with error: {str(e)}")
        raise e


def free_port(port_num):
    command = 'lsof -t -i:' + str(port_num)
    c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = c.communicate()
    if stdout == b'':
        return
    pids = stdout.decode().strip().split('\n')
    for pid in pids:
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass


def lunch_server():
    try:
        send_request()
    except ConnectionError:
        print('Server is not running, starting server ...')
        free_port(port_num=ENDPOINT_PORT)
        subprocess.Popen(["./twtask"], close_fds=True)
        time.sleep(3)


def dict_validation(list1, list2):
    pairs = zip(list1, list2)
    return not any(x != y for x, y in pairs)


if __name__ == "__main__":
    send_request()
