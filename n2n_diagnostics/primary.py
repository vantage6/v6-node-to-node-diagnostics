""" methods.py

This file contains all algorithm pieces that are executed on the nodes.
It is important to note that the master method is also triggered on a
node just the same as any other method.

When a return statement is reached the result is send to the central
server after encryption.
"""
import socket
from typing import Any, Dict, Tuple

from vantage6.tools.util import info
from time import sleep

MESSAGE = b'Hello Python\n'
ECHO_TASK = 'echo'
WAIT = 10


def echo(client, data, *args, **kwargs):
    organizations = client.get_organizations_in_my_collaboration()
    ids = [organization.get("id") for organization in organizations]

    # The input fot the algorithm is the same for all organizations
    # in this case
    info("Defining input parameters")
    input_ = {
        "method": "some_example_method",
    }

    # create a new task for all organizations in the collaboration.
    info("Dispatching node-tasks")
    task = client.create_new_task(input_={'method': ECHO_TASK}, organization_ids=ids)

    info(f'Waiting {WAIT} seconds for the algorithm containers to boot up...')
    sleep(WAIT)

    # Ip address and port of algorithm can be found in results model
    result_objects = client.get_results(task_id=task.get("id"))

    succeeded_echos = []

    info(f'Echoing to {len(result_objects)} algorithms...')
    for r in result_objects:
        ip, port = _get_address_from_result(r)

        info(f'Sending message to {ip}:{port}')
        succeeded_echos.append(_check_echo(ip, port))

        info(f'Succeeded echos: {succeeded_echos}')
    return succeeded_echos


def _get_address_from_result(result: Dict[str, Any]) -> Tuple[str, int]:
    address = result['node']['ip']
    port = result['port']

    return address, port


def _check_echo(host, port):
    info(f'Checking echo on {host}:{port}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(MESSAGE)
        response = s.recv(len(MESSAGE))
        return response == MESSAGE
