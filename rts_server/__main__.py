import asyncio
from rts_server.src.main import GameServer

server = GameServer()
try:
    asyncio.run(server.start())
except KeyboardInterrupt:
    print('\nServer stopped')
