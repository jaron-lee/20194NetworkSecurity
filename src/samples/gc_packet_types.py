"""
Team 9 Packet Types

"""
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, UINT8, BUFFER, BOOL
from playground.network.packet.fieldtypes.attributes import Optional

# TODO: enforce class typing

def create_game_init_packet(username):
    """
    Creates packet for initiating game
    """
    pkt = GameInitPacket(username=username)
    return pkt
    

def process_game_init(pkt):
    """
    Returns username from game init packet

    """
    return pkt.username

def create_game_require_pay_packet(unique_id, account, amount):
    """
    Produces packet requesting particular amount from the bank

    """
    pkt = GameRequirePayPacket(unique_id=unique_id, account=account, amount=amount)

    return pkt

def process_game_require_pay_packet(pkt):
    """

    """

    return pkt.unique_id, pkt.account, pkt.amount

def create_game_pay_packet(receipt, receipt_signature):

    pkt = GamePayPacket(receipt=receipt, receipt_signature=receipt_signature)

    return pkt


def process_game_pay_packet(pkt):

    return pkt.receipt, pkt.receipt_signature


def create_game_response(response, status):
    
    pkt = GameResponsePacket(response=response, status=status)

    return pkt

def process_game_response(pkt):

    return pkt.response, pkt.status


def create_game_command(command):

    pkt = GameCommandPacket(server_command=command)

    return pkt

def process_game_command(pkt):

    return pkt.command


class GameInitPacket(PacketType):
    DEFINITION_IDENTIFIER = "initpacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
            ("username", STRING)
    ]


class GameRequirePayPacket(PacketType):
    DEFINITION_IDENTIFIER = "requirepaypacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
            ("unique_id", STRING),
            ("account", STRING),
            ("amount", UINT8)

    ]

class GamePayPacket(PacketType):
    DEFINITION_IDENTIFIER = "paypacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("receipt", BUFFER),
        ("receipt_signature", BUFFER)
    ]

class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "commandpacket"# whatever you want
    DEFINITION_VERSION = "1.0"

    FIELDS = [
            ("command", STRING)
        # whatever you want here
    ]

    
    
class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "responsepacket" 
    DEFINITION_VERSION = "1.0"


    FIELDS = [
            ("response", STRING),
            ("status", STRING),
        # whatever you want here
    ]

