import vantage6.client as v6client

IMAGE = 'carrrier-harbor.carrier-mu.src.surf-hosted.nl/carrier/n2n-diagnostics'


class N2NDiagnosticsClient:

    def __init__(self, client: v6client.Client):
        self.client = client

    def echo(self, master_node, collaboration_id, exclude_orgs):
        exclude_orgs = [master_node] + list(exclude_orgs)
        task = self.client.task.create(collaboration=collaboration_id,
                                       organizations=[master_node],
                                       name='test_echo',
                                       image=IMAGE, description='test',
                                       input={'method': 'echo', 'master': True,
                                              'kwargs': {
                                                  'exclude_orgs': exclude_orgs}})

        return task
