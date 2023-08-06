from asyncio import create_task
from blacksheep import WebSocket
from kikiutils.json import odumps, oloads
from typing import Callable, Coroutine


class WebsocketConnection:
    code: str = ''

    def __init__(self, websocket: WebSocket):
        self.ws = websocket

    async def emit(self, event: str, *args, **kwargs):
        await self.ws.send_bytes(odumps([event, args, kwargs]))

    async def recv_data(self) -> list:
        data = await self.ws.receive_text()
        return oloads(data)


class Websockets:
    def __init__(self):
        self.connections: dict[str, dict[str, WebsocketConnection]] = {}
        self.event_handlers: dict[str, Callable[..., Coroutine]] = {}

    def _add_connection(self, user_code: str, connection: WebsocketConnection):
        if user_code not in self.connections:
            self.connections[user_code] = {}
        self.connections[user_code][connection.code] = connection

    def _del_connection(self, user_code: str, connection: WebsocketConnection):
        if user_code in self.connections:
            self.connections[user_code].pop(connection.code, None)

            if not len(self.connections[user_code]):
                self.connections.pop(user_code, None)

    async def _listen(self, connection: WebsocketConnection):
        while True:
            data = await connection.ws.receive_text()

            if data == '':
                continue

            event, args, kwargs = oloads(data)

            if event in self.event_handlers:
                create_task(
                    self.event_handlers[event](connection, *args, **kwargs)
                )

    async def accept_and_listen(self, user_code: str, websocket: WebSocket):
        await websocket.accept()

        try:
            connection = WebsocketConnection(websocket)
            data = await connection.recv_data()

            if data[0] != 'init' or 'code' not in data[2]:
                raise ValueError('')

            connection.code = data[2]['code']
            self._add_connection(user_code, connection)
            await self._listen(connection)
        except:
            pass

        self._del_connection(user_code, connection)

    async def emit_to_all(self, event: str, *args, **kwargs):
        data = odumps([event, args, kwargs])

        for ucs in self.connections.values():
            for c in ucs.values():
                await c.ws.send_bytes(data)

    async def emit_to_user(self, user_code: str, event: str, *args, **kwargs):
        if user_code is self.connections:
            data = odumps([event, args, kwargs])

            for c in self.connections[user_code].values():
                await c.ws.send_bytes(data)

    def on(self, event: str):
        def decorator(view_func):
            self.event_handlers[event] = view_func
            return view_func
        return decorator
