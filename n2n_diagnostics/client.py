import vantage6.client as v6client

IMAGE = 'harbor.carrier-mu.src.surf-hosted.nl/carrier/n2n-diagnostics'


class N2NDiagnosticsClient:

    def __init__(self, client: v6client.Client, image=IMAGE):
        self.client = client
        self.image = image

    def echo(self, master_node, collaboration_id, other_nodes):
        task = self.client.task.create(collaboration=collaboration_id,
                                       organizations=[master_node],
                                       name='test_echo',
                                       image=self.image, description='test',
                                       input={'method': 'echo', 'master': True,
                                              'kwargs': {
                                                  'other_nodes': other_nodes}})

        return task
