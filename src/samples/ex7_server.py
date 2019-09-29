import asyncio
import time
import functools
from escape_room_006 import EscapeRoomGame
import playground
from autograder_ex6_packets import AutogradeTestStatus
import gc_packet_types
from CipherUtil import loadCertFromFile
from BankCore import LedgerLineStorage, LedgerLine
from OnlineBank import BankClientProtocol, OnlineBankConfig
import getpass, sys, os, asyncio

from playground.common.logging import EnablePresetLogging, PRESET_DEBUG
EnablePresetLogging(PRESET_DEBUG)

bankconfig = OnlineBankConfig()
bank_addr =     bankconfig.get_parameter("CLIENT", "bank_addr")
bank_port = int(bankconfig.get_parameter("CLIENT", "bank_port"))
bank_stack     =     bankconfig.get_parameter("CLIENT", "stack","default")
bank_username  =     bankconfig.get_parameter("CLIENT", "username")

certPath = os.path.join(bankconfig.path(), "bank.cert")
bank_cert = loadCertFromFile(certPath)
SRC_ACCOUNT = "jlee662_account"

def verify(bank_client, receipt_bytes, signature_bytes, dst, amount, memo):
    if not bank_client.verify(receipt_bytes, signature_bytes):
        raise Exception("Bad receipt. Not correctly signed by bank")
    ledger_line = LedgerLineStorage.deserialize(receipt_bytes)
    if ledger_line.getTransactionAmount(dst) != amount:
        raise Exception("Invalid amount. Expected {} got {}".format(amount, ledger_line.getTransactionAmount(dst)))
    elif ledger_line.memo(dst) != memo:
        raise Exception("Invalid memo. Expected {} got {}".format(memo, ledger_line.memo()))
    return True

def write_function(self, string, transport, status):
    transport.write(
        create_game_response(
            response = string,
            status=status
            ).__serialize__()
        )
    print("S:", string)

class StudentServer(asyncio.Protocol):
    def __init__(self):
        username = "jlee662" # could override at the command line
        password = getpass.getpass("Enter password for {}: ".format(username))
        bank_client = BankClientProtocol(bank_cert, username, password) 
        self.bank_client = bank_client
        self.verification = False


    def connection_made(self, transport):
        print("S: connection made")
        self.transport = transport

        game = EscapeRoomGame()
        game.output = functools.partial(write_function, transport=self.transport, status=game.status)
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


        if isinstance(packet, gc_packet_types.GameInitPacket):
            username = gc_packet_types.process_game_init(packet)

            pay_packet = gc_packet_types.create_game_require_pay_packet(unique_id="graphchess",
                    account="jlee662_account",
                    amount=10)

            self.transport.write(
                    pay_packet.__serialize__()
            )
        elif isinstance(packet, gc_packet_types.GamePayPacket):
            receipt_bytes, signature_bytes = gc_packet_types.process_game_pay_packet(packet)
            try:
                verification = verify(
                        bank_client=self.bank_client, 
                        receipt_bytes=receipt_bytes, 
                        signature_bytes=signature_bytes, 
                        amount=10, 
                        memo="graphchess")
            except Exception as e:
                print(e)
                self.transport.write(
                    create_game_response_packet(
                        response="",
                        status="dead")
                )

                self.transport.close()

        elif isinstance(packet, gc_packet_types.AutogradeTestStatus)
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
