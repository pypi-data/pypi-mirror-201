import asyncio
from asyncio import StreamReader
from asyncio import StreamWriter
from logging import getLogger

logger = getLogger(__name__)


async def handle_client(reader: StreamReader, writer: StreamWriter):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info("peername")
    logger.info(f"Received {message!r} from {addr!r}")
    writer.write(data)
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def run_server():
    server = await asyncio.start_server(handle_client, "localhost", 9000)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    from logging import basicConfig
    from logging import getLogger

    from rich.logging import RichHandler

    basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])

    asyncio.run(run_server())
