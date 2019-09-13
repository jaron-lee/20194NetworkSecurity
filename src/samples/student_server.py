import asyncio
import time
import functools
from escape_room_001 import *
def write_function(string, conn):
    print(string)
    conn.write(string.encode())

class StudentServer(asyncio.Protocol):
    def __init__(self):
        pass
        #while game.status == "playing":
        #    data = conn.recv(1024)
        #    data_as_string = data.decode()
        #    lines = data_as_string.split("\n")
        #    for line in lines:
        #        if len(line) > 0:
        #            print(line)
        #            output = game.command(line)

    def connection_made(self, transport):
        self.transport = transport
        game = EscapeRoomGame(output=functools.partial(write_function, conn=self.transport))
        game.create_game()
        game.start()
        self.game = game

    def data_received(self, data):

        time.sleep(.2)
        text = data.decode()
        lines = text.split("<EOL>\n")
        if self.game.status == "playing":
            for line in lines:
                if len(line) > 0:
                    print(line)
                    output = self.game.command(line)

        
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
