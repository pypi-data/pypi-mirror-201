from asyncio import Task
from asyncio import create_task
from asyncio import sleep
from logging import getLogger
from typing import Any
from typing import Coroutine

logger = getLogger(__name__)


def run_every(delay: float, coroutine: Coroutine[None, None, None]) -> Task:
    """
    This function runs awaitable coroutine, with no arguments, every delay seconds.
    """

    async def _run_every():
        while True:
            try:
                await coroutine()
            except Exception as e:
                name = str(coroutine.__name__)
                logger.warn(f"[stated]: exception happened while running task {name}\n {e}")
            await sleep(delay)

    return create_task(_run_every())
