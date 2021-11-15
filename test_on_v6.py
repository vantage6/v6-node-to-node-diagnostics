#!/usr/bin/env python3

from pathlib import Path
from time import sleep
from typing import List

import clize
import vantage6.client as v6client

IMAGE = 'carrrier-harbor.carrier-mu.src.surf-hosted.nl/carrier/n2n-diagnostics'
RETRY = 5
SLEEP = 10
DEFAULT_METHOD = 'echo'


def test_on_v6(host: str, port: int, username: str, password: str, private_key: str,
               collaboration_id: int, *, method: str = DEFAULT_METHOD):
    client = v6client.Client(host, port, verbose=True)

    client.authenticate(username, password)
    client.setup_encryption(private_key)

    # Get organizations
    organizations = client.collaboration.list()[0]['organizations']
    print(organizations)

    org_ids = [o['id'] for o in organizations]
    master_node = org_ids[0]

    task = client.task.create(collaboration=collaboration_id, organizations=[master_node],
                              name='test_echo',
                              image=IMAGE, description='test',
                              input={'method': method, 'master': True,
                                     'kwargs': {'exclude_orgs': [master_node]}})
    print(task)

    result = {}
    for i in range(RETRY):

        for r in task['results']:
            result = client.result.get(r['id'])

            print(result)
            print('Result:')
            print(get_output(result))
            print()
            print('Log:')
            print(get_log(result))

        sleep(SLEEP)
        if result['finished_at']:
            break


def get_output(result):
    return result['result']


def get_log(result):
    return result['log']


if __name__ == '__main__':
    clize.run(test_on_v6)
