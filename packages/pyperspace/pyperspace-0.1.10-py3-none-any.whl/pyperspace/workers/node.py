import asyncio

class Node:
    async def open(self, tcp_host: str, tcp_port: int) -> None:
        self._rd, self._wr = asyncio.open_connection(tcp_host, tcp_port)
        self._read = self._rd.readexactly
        self._write = self._wr.write

    async def close(self) -> None:
        self._rd.close()
        self._wr.close()
        self._wr.wait_closed()

    async def read_message(self) -> bytes:
