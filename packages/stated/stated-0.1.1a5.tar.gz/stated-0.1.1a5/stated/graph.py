from dataclasses import dataclass
from typing import List

from stated.peer import Peer


@dataclass
class Edges:
    active: List[Peer]
    inactive: List[Peer]


@dataclass
class Graph:
    vertices: List[Peer]
    edges: Edges
