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
import traceback

MESSAGE = b'Hello Python\n'
ECHO_TASK = 'echo'
WAIT = 4
TIMEOUT = 20
ENDLESS_SLEEP = 10000
WAIT_TASK = 'wait'
RETRY = 10


def echo(client, data, exclude_orgs=None, **kwargs):
    try:
        return try_echo(client, exclude_orgs)
    except Exception as e:
        info('Exception!')
        info(traceback.format_exc())
        raise e


def wait(client, data, exclude_orgs=None, **kwargs):
    ids = get_secondary_organizations(client, exclude_orgs)
    info("Dispatching node-tasks")
    task = client.create_new_task(input_={'method': WAIT_TASK}, organization_ids=ids)
    sleep(ENDLESS_SLEEP)


def try_echo(client, exclude_orgs):
    ids = get_secondary_organizations(client, exclude_orgs)
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

    # Ip address and port of algorithm can be found in results model
    addresses = _await_port_numbers(client, task.get('id'))
    succeeded_echos = []
    info(f'Echoing to {len(addresses)} algorithms...')

    for ip, port in addresses:

        info(f'Sending message to {ip}:{port}')
        succeeded_echos.append(_check_echo(ip, port))

        info(f'Succeeded echos: {succeeded_echos}')
    return succeeded_echos


def _await_port_numbers(client, task_id):
    result_objects = client.get_other_node_ip_and_port(task_id=task_id)
    c = 0
    while len(list(_get_available_addresses(result_objects))) < len(result_objects):
        if c >= RETRY:
            info('Cannot contact all organizations!')
            break

        info('Polling results for port numbers...')
        result_objects = client.get_other_node_ip_and_port(task_id=task_id)
        c += 1
        sleep(4)

    return list(_get_available_addresses(result_objects))


def _get_available_addresses(result_objects)  -> Tuple[int, str]:
    for r in result_objects:
        ip, port = _get_address_from_result(r)
        if port:
            yield ip, port


def get_secondary_organizations(client, exclude_orgs):
    organizations = client.get_organizations_in_my_collaboration()
    info(str(exclude_orgs))
    ids = [organization.get('id') for organization in organizations]
    if exclude_orgs:
        ids = [i for i in ids if i not in exclude_orgs]
    return ids


def _get_address_from_result(result: Dict[str, Any]) -> Tuple[str, int]:
    address = result['ip']
    port = result['port']

    return address, port


def _check_echo(host, port):
    info(f'Checking echo on {host}:{port}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT)
        s.connect((host, port))
        s.sendall(MESSAGE)
        response = s.recv(len(MESSAGE))
        return response == MESSAGE
