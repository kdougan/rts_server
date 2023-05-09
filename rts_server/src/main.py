import os
import asyncio
import itertools
import time
from dataclasses import asdict

import orjson
import websockets
from websockets.server import WebSocketServerProtocol

from rts_server.src.lib import GameState

from dotenv import load_dotenv

load_dotenv()


class GameServer:
    tick_rate = int(os.getenv('TICK_RATE', 24))
    game_state = GameState()
    connections = set()

    async def start(self):

        server = await websockets.serve(  # type: ignore
            self.handle_client, 'localhost', 8765)
        print('Server started at ws://localhost:8765')

        await asyncio.gather(server.wait_closed(), self.game_loop())

    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        player_id = self.register_player(websocket)
        await self.send_message(websocket, asdict(self.game_state))
        try:
            async for message in websocket:
                data = orjson.loads(message)
                self.process_client_message(player_id, data)
        finally:
            self.unregister_player(websocket)

    def register_player(self, websocket: WebSocketServerProtocol):
        player_id = len(self.connections) + 1
        self.connections.add(websocket)
        return player_id

    def unregister_player(self, websocket: WebSocketServerProtocol):
        if websocket.id in self.game_state.players:
            del self.game_state.players[websocket.id]
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def send_message(self, websocket: WebSocketServerProtocol, message: dict):
        await websocket.send(orjson.dumps(message))

    def process_client_message(self, player_id: int, message: dict):
        pass

    async def game_loop(self):
        moon = itertools.cycle(['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'])
        while True:
            print(next(moon), end='\r')
            current_time = int(time.time())
            await self.update_game_state(current_time)
            await self.broadcast_game_state()
            await asyncio.sleep(1/self.tick_rate)

    async def update_game_state(self, current_time: int):
        pass

    async def broadcast_game_state(self):
        pass
