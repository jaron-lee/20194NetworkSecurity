import asyncio
import time
import functools
from escape_room_006 import *
import playground
from 06_game_packet_types import *

def write_function(string, conn):
    print("SS: ", string)
    string = string + "<EOL>\n"
    response = GameResponsePacket(server_response=string,
            server_status="Success")
    conn.write(string.__serialize__())

def new_write_function(string, responses):
    responses.append(string)

class StudentServer(asyncio.Protocol):
    def __init__(self):
        responses = []
        pass

    #async def wait_agents(self):
    #    await asyncio.wait([asyncio.create_task(a) for a in self.game.agents])

    def connection_made(self, transport):
        print("S: connection made")
        self.transport = transport
        game = EscapeRoomGame(output=functools.partial(new_write_function, responses=self.responses))
        game.responses = []
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
        #if self.game.status == "playing":
        if self.game.status == "playing":
            game_running = True
        else:
            game_running = False
        for line in lines:
            if len(line) > 0:
                print("S: ", line)
                self.game.command(line)

                self.transport.write(
                        GameResponsePacket(
                            server_response = self.responses[-1],
                            server_status="Success"
                            game_running=game_running
                            )
                        )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = playground.create_server(StudentServer,"localhost", 1290)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_close())
    loop.close()
