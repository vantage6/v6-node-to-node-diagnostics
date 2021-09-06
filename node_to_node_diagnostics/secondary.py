import asyncio

from vantage6.tools.util import info

DEFAULT_PORT = 9999
LOCALHOST = '127.0.0.1'


def RPC_echo(data, *args, **kwargs):
    """
    Start echo socket server
    """
    asyncio.run(_serve_echo())


async def _serve_echo():
    info('Start')
    server = await asyncio.start_server(_handle_echo, LOCALHOST, DEFAULT_PORT)

    async with server:
        await server.serve_forever()


async def _handle_echo(reader, writer):
    # Read message
    line = await reader.readline()

    info(f'Received {line.decode()}')
    writer.writelines([line])
    await writer.drain()

    print('Close the connection')
    writer.close()


if __name__ == '__main__':
    RPC_echo(None)
