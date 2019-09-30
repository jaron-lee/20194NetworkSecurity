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
    Returns username (STRING) from GameInitPacket

    """
    assert isinstance(pkt, GameInitPacket)
    return pkt.username

def create_game_require_pay_packet(unique_id, account, amount):
    """
    Produces packet requesting particular amount from the bank

    """
    
    pkt = GameRequirePayPacket(unique_id=unique_id, account=account, amount=amount)

    return pkt

def process_game_require_pay_packet(pkt):
    """
    Returns unique_id (STRING), account (STRING), amount (UINT8) from GameRequirePayPacket
    """
    assert isinstance(pkt, GameRequirePayPacket)

    return pkt.unique_id, pkt.account, pkt.amount

def create_game_pay_packet(receipt, receipt_signature):
    """
    Prove payment to the bank
    """

    pkt = GamePayPacket(
            receipt=receipt, receipt_signature=receipt_signature
            )

    return pkt


def process_game_pay_packet(pkt):
    """
    Returns receipt (BUFFER), receipt_signature (BUFFER) from GamePayPacket

    """
    assert isinstance(pkt, GamePayPacket)

    return pkt.receipt, pkt.receipt_signature


def create_game_response(response, status):
    """
    Conveys game response 

    """
    
    pkt = GameResponsePacket(response=response, status=status)

    return pkt

def process_game_response(pkt):
    """
    Returns response (STRING) and status (STRING)

    """
    assert isinstance(pkt, GameResponsePacket)

    return pkt.response, pkt.status


def create_game_command(command):
    """
    Conveys game command

    """
    pkt = GameCommandPacket(command=command)

    return pkt

def process_game_command(pkt):
    """
    Returns command (STRING)
    """
    assert isinstance(pkt, GameCommandPacket)

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
    DEFINITION_IDENTIFIER = "commandpacket"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
            ("command", STRING)
    ]

    
    
class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "responsepacket" 
    DEFINITION_VERSION = "1.0"


    FIELDS = [
            ("response", STRING),
            ("status", STRING),
    ]

