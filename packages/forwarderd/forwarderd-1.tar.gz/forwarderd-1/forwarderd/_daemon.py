import asyncio
import logging

from threading import Lock
from traceback import format_exc

from paramiko import RSAKey
from sshtunnel import SSHTunnelForwarder

from ._shared import (
    MessageType,
    SpawnTunnelData,
    SpawnTunnelResponse,
    asdict, load_frame, dump_frame, start_server
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S'
)
logger = logging.getLogger()


spawn_lock = Lock()
spawned: 'dict[tuple, SSHTunnelForwarder]' = {}


def blocking_spawn(data: SpawnTunnelData):
    with spawn_lock:
        forwarder_id = (data.ssh_addr, data.ssh_user)
        print(forwarder_id)
        if spawned_forwarder := spawned.get(forwarder_id):
            return spawned_forwarder

        key = RSAKey.from_private_key_file(data.ssh_identity_file)
        forwarder = SSHTunnelForwarder(
            ssh_address_or_host=data.ssh_addr,
            ssh_username=data.ssh_user,
            ssh_pkey=key,
            remote_bind_address=data.remote_addr,
            local_bind_address=('localhost',)
        )
        forwarder.start()

        logger.info('New forwarder spawned (ssh_addr=%s, remote_addr=%s)',
                    data.ssh_addr, data.remote_addr)

        spawned[forwarder_id] = forwarder
        return forwarder


async def spawn_tunnel(data: SpawnTunnelData):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, blocking_spawn, data)


async def handle_request(req_type: MessageType, data):
    if req_type == MessageType.SPAWN_TUNNEL:
        data = SpawnTunnelData(**data)
        forwarder = await spawn_tunnel(data)
        response = SpawnTunnelResponse(
            address=forwarder.local_bind_address
        )
        return (MessageType.OK, asdict(response))

    else:
        raise ValueError(f'Unknown request {req_type!r}')


async def on_connect(r: asyncio.StreamReader, w: asyncio.StreamWriter):
    req_type, req_data = load_frame(await r.readline())
    try:
        resp_type, resp_data = await handle_request(req_type, req_data)
    except Exception as e:
        logger.error(format_exc())
        resp_type = MessageType.ERROR
        resp_data = {'error': repr(e)}

    w.write(dump_frame(resp_type, resp_data))
    await w.drain()
    w.close()
    await w.wait_closed()


async def main():
    server = await start_server(on_connect)
    logger.info('Server started!')
    try:
        await server.serve_forever()
    except KeyboardInterrupt:
        server.close()
        await server.wait_closed()
        logger.info('Server closed.')
