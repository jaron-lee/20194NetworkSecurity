import asyncio
import playground
import time
from autograder_ex6_packets import *
from playground.network.packet import PacketType
from ex6_game_packet_types import *

from playground.common.logging import EnablePresetLogging, PRESET_VERBOSE
EnablePresetLogging(PRESET_VERBOSE)

class StudentClient(asyncio.Protocol):
    def __init__(self):
        self.instruction_counter = 0
        self.instructions = [
                            "look mirror", 
                            "get hairpin",
                            "unlock chest with hairpin",
                            "open chest",
                            "get hammer from chest",
                            "hit flyingkey with hammer",
                            "get key",
                            "unlock door with key",
                            "open door"]

    def connection_made(self, transport):
        self.transport = transport
        self.d = PacketType.Deserializer()
        #start_packet = AutogradeStartTest(
        #        name="Jaron Lee",
        #        team=9,
        #        email="jaron.lee@jhu.edu",
        #        port=7816,
        #        packet_file=b""
        #        )
        #self.transport.write(start_packet.__serialize__())
        print("C: Sent packet")
        #self.transport.write("Hello World".encode())


    def data_received(self, data):
        print("C: Received packet")
        self.d.update(data)
        for packet in self.d.nextPackets():
            if packet.DEFINITION_IDENTIFIER == "20194.exercise6.autogradesubmitresponse":
                if packet.submit_status != AutogradeTestStatus.PASSED:
                    print(packet.error)
            elif packet.DEFINITION_IDENTIFIER == "exercise6.jaron.response":
                text = packet.server_response
                print(text)
                if packet.game_over():
                    print("C: GAME OVER")

                elif self.instruction_counter < len(self.instructions):
                    #if self.instruction_counter < len(self.instructions):
                    if self.instructions[self.instruction_counter] == "hit flyingkey with hammer":
                        if text.split("<EOL>\n")[0].endswith("wall"):
                            instruction = self.instructions[self.instruction_counter] + "<EOL>\n"
                            self.transport.write(
                                    GameCommandPacket(
                                        command=instruction
                                        ).__serialize__()
                                    )
                            self.instruction_counter += 1
                    else:
                        instruction = self.instructions[self.instruction_counter] + "<EOL>\n"

                        print("C: {}".format(instruction))
                        self.transport.write(
                                GameCommandPacket(
                                    command=instruction
                                    ).__serialize__()
                                )
                        self.instruction_counter += 1


        #text = data.decode()
        #print("CR: ", text)
        #time.sleep(.2)
        #if self.instruction_counter < len(self.instructions):
        #    if text == "SUBMIT autograde command:<EOL>\n":
        #        print("C: submit request")
        #        self.transport.write("SUBMIT,Jaron Lee,jaron.lee@jhu.edu,9,1290<EOL>\n".encode())
        #    if text.startswith("SUBMIT: OK"):
        #        test_id = text.split(",")[1]
        #        print("C: success, {}".format(test_id))
        #    if self.instructions[self.instruction_counter] == "hit flyingkey with hammer":
        #        if text.split("<EOL>\n")[0].endswith("wall"):
        #            instruction = self.instructions[self.instruction_counter] + "<EOL>\n"
        #            self.transport.write(instruction.encode())
        #            self.instruction_counter += 1
        #    else:
        #        instruction = self.instructions[self.instruction_counter] + "<EOL>\n"
        
        #        print("C: {}".format(instruction))
        #        self.transport.write(instruction.encode())
        #        self.instruction_counter += 1
        #else:
        #    print("RAN OUT OF INSTRUCTIONS!")


         

if __name__ == "__main__":
    time.sleep(1)

    loop = asyncio.get_event_loop()
    coro = playground.create_connection(StudentClient,'127.0.0.1',1292)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    client.close()
    loop.run_until_complete(client.close())
    loop.close()
