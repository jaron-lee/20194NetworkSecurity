import asyncio
import playground
import time
from autograder_ex6_packets import AutogradeStartTest, AutogradeTestStatus
from playground.network.packet import PacketType
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

async def transfer(bank_client, src, dst, amount, memo):
    await playground.create_connection(
            lambda: bank_client,
            bank_addr,
            bank_port,
            family='default'
            )
    print("Connected. Logging in.")
        
    try:
        await bank_client.loginToServer()
    except Exception as e:
        print("Login error. {}".format(e))
        return False

    try:
        await bank_client.switchAccount(src)
    except Exception as e:
        print("Could not set source account as {} because {}".format(
            src,
            e))
        return False
    
    try:
        result = await bank_client.transfer(dst, amount, memo)
    except Exception as e:
        print("Could not transfer because {}".format(e))
        return False
    
    return result

class StudentClient(asyncio.Protocol):
    def __init__(self):
        self.instruction_counter = 0
        self.instructions = [
                            "look mirror", 
                            "get hairpin",
                            "unlock chest with hairpin",
                            "open chest",
                            "look in chest",
                            "get hammer from chest",
                            "hit flyingkey with hammer",
                            "get key",
                            "unlock door with key",
                            "open door"]

    def connection_made(self, transport):
        self.transport = transport
        #d = PacketType.Deserializer()
        #self.d = d
        start_packet = AutogradeStartTest(
                name="Jaron Lee",
                team=9,
                email="jaron.lee@jhu.edu",
                port=7826
                )
        with open("gc_packet_types.py", "rb") as f:
            start_packet.packet_file = f.read()
        self.transport.write(start_packet.__serialize__())
        print("C: Sent Autograde packet")
        #self.transport.write("Hello World".encode())

    def data_received(self, data):
        print("C: Received packet")
        d = PacketType.Deserializer()
        d.update(data)
        packets = list(d.nextPackets())
        packet = packets[0]
        print(packet)
        time.sleep(.5)
    

        print("C: New packet - ", packet.DEFINITION_IDENTIFIER)
        if isinstance(packet, AutogradeTestStatus):
            print("C: {}".format(packet.test_id))
            print("C: SUBMITRESPONSE {} {} {}".format(packet.submit_status, packet.client_status, packet.server_status))
            

            if packet.submit_status == AutogradeTestStatus.PASSED:
                request_start_packet = gc_packet_types.create_game_init_packet(username="jlee662")
                print("C: {}".format(request_start_packet.DEFINITION_IDENTIFIER))
                self.transport.write(
                        request_start_packet.__serialize__()
                )
                print("C: Sent game start packet")
            #if packet.submit_status != AutogradeTestStatus.PASSED:
            #    print(packet.error)
        elif isinstance(packet, gc_packet_types.GameRequirePayPacket):
            unique_id, account, amount = gc_packet_types.process_game_require_pay_packet(packet)

            payment_result = await transfer(
                    bank_client=bank_client, 
                    src=SRC_ACCOUNT,
                    dst=account,
                    amount=amount,
                    memo=unique_id)
            print("C: Paid {} to {}".format(amount, account))

            if payment_result:
                pay_packet = gc_packet_types.create_game_pay_packet(
                        receipt=payment_result.Receipt,
                        receipt_signature=payment_result.ReceiptSignature)

                self.transport.write(
                        pay_packet.__serialize__()
                )



        elif isinstance(packet, gc_packet_types.GameResponsePacket):
            text = packet.server_response
            print("C :", text)
            if packet.game_over():
                print("C: GAME OVER - safe to terminate")

            elif self.instruction_counter < len(self.instructions):
                #if self.instruction_counter < len(self.instructions):
                if self.instructions[self.instruction_counter] == "hit flyingkey with hammer":
                    if text.split("<EOL>\n")[0].endswith("wall"):
                        instruction = self.instructions[self.instruction_counter]# + "<EOL>\n"
                        print("CS: {}".format(instruction))
                        self.transport.write(
                                GameCommandPacket(
                                    server_command=instruction
                                    ).__serialize__()
                                )
                        self.instruction_counter += 1
                else:
                    instruction = self.instructions[self.instruction_counter] #+ "<EOL>\n"

                    print("CS: {}".format(instruction))
                    self.transport.write(
                            GameCommandPacket(
                                server_command=instruction
                                ).__serialize__()
                            )
                    self.instruction_counter += 1
        else:
            raise ValueError(packet.DEFINITION_IDENTIFIER)



if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    coro = playground.create_connection(StudentClient,'20194.0.0.19000',19007)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    client.close()
    loop.run_until_complete(client.close())
    loop.close()
