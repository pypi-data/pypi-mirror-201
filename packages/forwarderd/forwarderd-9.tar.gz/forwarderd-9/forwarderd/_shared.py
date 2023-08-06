# pyright: reportGeneralTypeIssues=false

import os
import json
import asyncio

from enum import Enum
from dataclasses import dataclass, asdict


IP_ADDR = ('localhost', 19567)
SOCK_PATH = '/var/run/forwarderd.sock'


if hasattr(asyncio, 'open_unix_connection'):
    async def connect():
        return await asyncio.open_unix_connection(SOCK_PATH)

    async def start_server(cb):
        os.makedirs(os.path.dirname(SOCK_PATH), exist_ok=True)
        server = await asyncio.start_unix_server(cb, SOCK_PATH)
        os.chmod(SOCK_PATH, 0o777)
        return server

else:
    async def connect():
        return await asyncio.open_connection(*IP_ADDR)

    async def start_server(cb):
        return await asyncio.start_server(cb, *IP_ADDR)


def dump_frame(type: 'MessageType', data: dict) -> bytes:
    str_dump = json.dumps([type, data], ensure_ascii=False)
    return str_dump.encode('utf-8') + b'\n'


def load_frame(data: bytes) -> 'tuple[MessageType, dict]':
    return tuple(json.loads(data[:-1]))


class MessageType(int, Enum):
    SPAWN_TUNNEL = 1

    OK = 15
    ERROR = 16


@dataclass
class SpawnTunnelRequest:
    ssh_addr: str
    ssh_user: str
    ssh_identity_file: str
    remote_addr: str
    local_addr: str = ''


@dataclass
class SpawnTunnelResponse:
    host: str
    port: int
