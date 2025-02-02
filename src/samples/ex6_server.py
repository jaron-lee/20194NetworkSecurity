import asyncio
import time
import functools
from escape_room_006 import EscapeRoomGame
import playground
from ex6_game_packet_types import GameCommandPacket, GameResponsePacket
from autograder_ex6_packets import *

from playground.common.logging import EnablePresetLogging, PRESET_DEBUG
EnablePresetLogging(PRESET_DEBUG)

def write_function(self, string, transport, status):
    # This is not good engineering
    # How to pass the game status inside this function?
    if string.startswith("VICTORY"):
        status = "escaped"
    transport.write(
        GameResponsePacket(
            server_response = string,
            server_status=status
            ).__serialize__()
        )
    print("S:", string)

class StudentServer(asyncio.Protocol):
    def __init__(self):
        self.status = None
        print("S: server started")


    def connection_made(self, transport):
        print("S: connection made")
        self.transport = transport

        game = EscapeRoomGame(output=functools.partial(write_function, transport=self.transport, status=self.status))
        game.create_game()
        game.start()
        self.game = game
        #asyncio.create_task(self.wait_agents())
        for a in game.agents:
            asyncio.ensure_future(a)
        print("S: packet sent")

    def connection_lost(self, ex):
        print("S: closing transport")
        self.transport.close()

    def data_received(self, data):
        print("S: Received packet")
        d = PacketType.Deserializer()
        d.update(data)
        packets = list(d.nextPackets())
        packet = packets[0]
        if packet.DEFINITION_IDENTIFIER == "jaroncommandpacket":
            print("SR: ", packet.command())
            text = packet.command()

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
    coro = playground.create_server(StudentServer, port=7826)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_close())
    loop.close()
