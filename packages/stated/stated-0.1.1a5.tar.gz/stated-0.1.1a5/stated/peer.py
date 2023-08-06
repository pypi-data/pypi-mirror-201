from dataclasses import dataclass


@dataclass
class Peer:
    ip: str
    port: int
    host: str
    proximity: int


async def connect_to_peer(peer: Peer):
    pass
