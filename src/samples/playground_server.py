import asyncio
import time
import functools
from escape_room_004 import *
import playground

def write_function(string, conn):
    print("SS: ", string)
    conn.write(string.encode())

class StudentServer(asyncio.Protocol):
    def __init__(self):
        pass

    #async def wait_agents(self):
    #    await asyncio.wait([asyncio.create_task(a) for a in self.game.agents])

    def connection_made(self, transport):
        print("S: connection made")
        self.transport = transport
        game = EscapeRoomGame(output=functools.partial(write_function, conn=self.transport))
        game.create_game()
        game.start()
        self.game = game
        #asyncio.create_task(self.wait_agents())
        for a in game.agents:
            asyncio.ensure_future(a)

    def connection_lost(self, ex):
        print("S: closing transport")
        self.transport.close()

    def data_received(self, data):
        text = data.decode()
        print("SR: ", text)
        asyncio.sleep(.2)
        lines = text.split("<EOL>\n")
        if self.game.status == "playing":
            for line in lines:
                if len(line) > 0:
                    print("S: ", line)
                    self.game.command(line)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = playground.create_server(StudentServer,"localhost", 1091)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_close())
    loop.close()
