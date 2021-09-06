""" methods.py

This file contains all algorithm pieces that are executed on the nodes.
It is important to note that the master method is also triggered on a
node just the same as any other method.

When a return statement is reached the result is send to the central
server after encryption.
"""
import socket
from vantage6.tools.util import info

from node_to_node_diagnostics import mock

MESSAGE = b'Hello Python\n'


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
    task = mock.create_new_task(ids)

    # Retrieve address of algorithm
    result_objects = mock.get_results(task_id=task.get("id"))

    succeeded_echos = [_check_echo(mock.get_node_address(r), r['port']) for r in result_objects]

    info(f'Succeeded echos: {succeeded_echos}')
    return succeeded_echos


def _check_echo(host, port):
    info(f'Checking echo on {host}:{port}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(MESSAGE)
        response = s.recv(len(MESSAGE))
        return response == MESSAGE
