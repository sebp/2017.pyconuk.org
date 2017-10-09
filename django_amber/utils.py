from multiprocessing import Process
from time import sleep
from socket import socket
import traceback

import requests

from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunserverCommand


default_port = RunserverCommand.default_port


def run_runserver_in_process(port=default_port):
    p = Process(
        target=call_command,
        args=('runserver', port),
        kwargs={'use_reloader': False},
    )

    p.start()

    wait_for_server(port)

    return p


def wait_for_server(port=default_port):
    get_with_retries('http://localhost:{}/'.format(port))


def get_with_retries(url, num_retries=5):
    for i in range(num_retries):
        try:
            rsp = requests.get(url)
            rsp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print('get_with_retries', i)
            traceback.print_exc()

        sleep(0.2 * 2 ** i)

    requests.get(url)


def get_free_port():
    s = socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return str(port)
