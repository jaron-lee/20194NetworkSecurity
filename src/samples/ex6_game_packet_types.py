from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import STRING, UINT8, BUFFER, BOOL
from playground.network.packet.fieldtypes.attributes import Optional

class GameCommandPacket(PacketType):
    DEFINITION_IDENTIFIER = "exercise6.jaron.command"# whatever you want
    DEFINITION_VERSION = "1.0"

    FIELDS = [
            ("command", STRING)
        # whatever you want here
    ]

    @classmethod
    def create_game_command_packet(cls, s):
        return cls(command=s.command)# whatever arguments needed to construct the packet)
    
    def command(self):
        return self.command# whatever you need to get the command for the game
    
class GameResponsePacket(PacketType):
    DEFINITION_IDENTIFIER = "exercise6.jaron.response" 
    DEFINITION_VERSION = "1.0"


    FIELDS = [
            ("server_response", STRING),
            ("server_status", STRING),
        # whatever you want here
    ]

    @classmethod
    def create_game_response_packet(cls, response, status):
        return cls(response=response, status=status) # whatever you need to construct the packet )
    
    def game_over(self):
        return self.server_status in ("dead", "escaped")# whatever you need to do to determine if the game is over
    
    def status(self):
        return self.server_status# whatever you need to do to return the status
    
    def response(self):
        return self.server_response# whatever you need to do to return the response

