from vantage6.tools.mock_client import ClientMockProtocol
from node_to_node_diagnostics import primary

## Mock client
client = ClientMockProtocol(["local/data.csv", "local/data.csv"], "node_to_node_diagnostics")


def main():
    primary.echo(client, None)


if __name__ == '__main__':
    main()
