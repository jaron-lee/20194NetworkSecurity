import asyncio
import time
import functools
from escape_room_006 import *
import playground
from ex6_game_packet_types import *

from playground.common.logging import EnablePresetLogging, PRESET_VERBOSE
EnablePresetLogging(PRESET_VERBOSE)

def new_write_function(string, transport, status):
    string = string + "<EOL>\n"
    transport.write(
            GameResponsePacket(
                server_response = string,
                server_status=status
                ).__serialize__()
            )
    print(string)

class StudentServer(asyncio.Protocol):
    def __init__(self):
        print("S: server started")
        self.responses = []
        self.status = None

    #async def wait_agents(self):
    #    await asyncio.wait([asyncio.create_task(a) for a in self.game.agents])

    def connection_made(self, transport):
        print("S: connection made")
        self.transport = transport
        game = EscapeRoomGame(output=functools.partial(new_write_function, transport=self.transport, status = self.status))
        game.create_game()
        game.start()
        self.game = game
        #asyncio.create_task(self.wait_agents())
        for a in game.agents:
            asyncio.ensure_future(a)
        self.d = PacketType.Deserializer()
        print("S: packet sent")

    def connection_lost(self, ex):
        print("S: closing transport")
        self.transport.close()

    def data_received(self, data):
        self.d.update(data)
        for packet in self.d.nextPackets():
            if packet.DEFINITION_IDENTIFIER == "exercise6.jaron.command":
                print("SR: ", packet.command)
                text = packet.command

            elif packet.DEFINITION_IDENTIFIER == "20194.exercise6.autogradesubmitresponse":
                print("S: SUBMITRESPONSE {} {} {}".format(packet.submit_status, packet.client_status, packet.server_status))
            else:
                raise ValueError(packet.DEFINITION_IDENTIFIER)

            time.sleep(.2)
            lines = text.split("<EOL>\n")
            #if self.game.status == "playing":
            for line in lines:
                if len(line) > 0:
                    print("S: ", line)
                    self.game.command(line)
                    self.status = self.game.status


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = playground.create_server(StudentServer,"localhost", 7816)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_close())
    loop.close()
