import asyncio
import itertools
import os
import time
from dataclasses import asdict
from typing import Any

import orjson
import websockets
from dotenv import load_dotenv
from websockets.server import WebSocketServer
from websockets.server import WebSocketServerProtocol

from rts_server.src.lib import GameState

load_dotenv()


class GameServer:
    tick_rate: int = int(os.getenv('TICK_RATE', 24))
    game_state: GameState = GameState()
    connections: set = set()

    async def start(self):
        '''Starts the server and game loop.'''
        server: WebSocketServer = await websockets.serve(  # type: ignore
            self.handle_client, 'localhost', 8765)
        print('Server started at ws://localhost:8765')

        await asyncio.gather(server.wait_closed(), self.game_loop())

    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        '''Handles a client connection.

        Args:
            websocket (WebSocketServerProtocol):
                The client connection.
            path (str):
                The path of the client.
        '''
        player_id: int = self.register_player(websocket)
        await self.send_message(websocket, asdict(self.game_state))
        try:
            async for message in websocket:
                data: dict[str, Any] = orjson.loads(message)
                self.process_client_message(player_id, data)
        finally:
            self.unregister_player(websocket)

    def register_player(self, websocket: WebSocketServerProtocol) -> int:
        '''Registers a player to the game.

        Args:
            websocket (WebSocketServerProtocol):
                The player connection.

        Returns:
            int: The player id.
        '''
        player_id: int = len(self.connections) + 1
        self.connections.add(websocket)
        return player_id

    def unregister_player(self, websocket: WebSocketServerProtocol):
        '''Unregisters a player from the game.

        Args:
            websocket (WebSocketServerProtocol):s
                The player connection.
        '''
        if websocket.id in self.game_state.players:
            del self.game_state.players[websocket.id]
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def send_message(self, websocket: WebSocketServerProtocol, message: dict):
        '''Sends a message to a client.

        Args:
            websocket (WebSocketServerProtocol):
                The player connection.
            message (dict):
                The message to send.
        '''
        await websocket.send(orjson.dumps(message))

    def process_client_message(self, player_id: int, message: dict):
        """Processes a message from a client.

        Args:
            player_id (int):
                The player id.
            message (dict):
                The message to process.
        """
        pass

    async def game_loop(self):
        """The game loop.
        """
        moon: itertools.cycle = itertools.cycle(
            ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'])
        while True:
            print(next(moon), end='\r')
            current_time: int = int(time.time())
            await self.update_game_state(current_time)
            await self.broadcast_game_state()
            await asyncio.sleep(1/self.tick_rate)

    async def update_game_state(self, current_time: int):
        """Updates the game state.

        Args:
            current_time (int):
                The current time.
        """
        pass

    async def broadcast_game_state(self):
        """Broadcasts the game state to all clients.
        """
        pass
