from ._shared import (
    MessageType,
    SpawnTunnelRequest,
    SpawnTunnelResponse,
    asdict, load_frame, dump_frame, connect
)


async def _make_request(req_type, req_data):
    r, w = await connect()

    w.write(dump_frame(req_type, req_data))
    resp_type, resp_data = load_frame(await r.readline())

    if resp_type == MessageType.ERROR:
        raise Exception(resp_data['error'])
    elif resp_type == MessageType.OK:
        return resp_data
    else:
        raise ValueError(f'Unknown response type {resp_type!r}')


async def spawn_tunnel(data: SpawnTunnelRequest) -> SpawnTunnelResponse:
    resp = await _make_request(MessageType.SPAWN_TUNNEL, asdict(data))
    return SpawnTunnelResponse(**resp)
