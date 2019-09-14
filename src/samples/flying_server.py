import asyncio
import time
import functools
from escape_room_004 import *
def write_function(string, conn):
    print(string)
    conn.write(string.encode())

class StudentServer(asyncio.Protocol):
    def __init__(self):
        pass

    def connection_made(self, transport):
        self.transport = transport
        loop = asyncio.get_event_loop()
        game = EscapeRoomGame(output=functools.partial(write_function, conn=self.transport))
        game.create_game()
        game.start()
        self.game = game
        self.loop = loop

        await asyncio.wait([asyncio.ensure_future(a) for a in self.game.agents])

    def data_received(self, data):
        text = data.decode()
        asyncio.sleep(.2)
        lines = text.split("<EOL>\n")
        if self.game.status == "playing":
            for line in lines:
                if len(line) > 0:
                    print(line)
                    self.game.command(line)

        
        #self.transport.write(data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = loop.create_server(StudentServer,'',1092)
    server = loop.run_until_complete(coro)

    

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_close())
    loop.close()
