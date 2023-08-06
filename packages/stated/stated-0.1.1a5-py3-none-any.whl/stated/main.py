from __future__ import annotations

from logging import getLogger
from os import getenv
from typing import List
from typing import Dict
from typing import Any

from stated.finder import Finder
from stated.peer import Peer
from stated.utils import run_every

logger = getLogger(__name__)

logger.debug("[stated]: imported")


class Stated:
    def __init__(self, agent_name: str | None = None, finders: List[Finder] = list()):
        logger.info("[stated]: initializing stated agent")
        self.blocks = []
        self.scan_interval = 1
        self.agent_name = agent_name or self.find_agent_name()
        self.peers: List[Peer] = list()
        self.finders: List[Finder] = list()
        self.graph_integrity_intervals = 1
        self.sync_intervals = 1

    async def get(self, id: str = None, query: Dict[str, Any] = None):
        logger.debug("[stated]: getting from state")
    
    async def put(self, data: Dict[str, Any]):
        logger.debug("[stated]: putting to state")


    def find_agent_name(self):
        return getenv("HOSTNAME", "stated-default")

    async def start(self) -> Stated:
        self.task_graph_integrity = run_every(self.graph_integrity_intervals, self.graph_integrity)
        self.task_sync_records = run_every(self.sync_intervals, self.sync_records)
        return self

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return await self.ensure_teardown()

    async def flush_backlog(self):
        logger.info("[stated]: flushing backlog")

    async def ensure_teardown(self):
        await self.flush_backlog()
        self.task_graph_integrity.cancel()
        self.task_sync_records.cancel()
        return self

    async def sync_records(self):
        logger.debug("[stated]: synchronizing records with peers")

    async def graph_integrity(self):
        logger.debug("[stated]: agent finder started")
        try:
            await self.heartbeat()
            await self.check_graph_integrity()

        except Exception as e:
            logger.error(f"[stated]: error finding other agents: {e}")

    async def heartbeat(self):
        logger.debug("[stated]: sending heartbeat to connected peers")
        # TODO:

    async def check_graph_integrity(self):
        logger.debug("[stated]: checking graph integrity")
