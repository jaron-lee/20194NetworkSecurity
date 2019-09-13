import asyncio
import time

class StudentClient(asyncio.Protocol):
    def __init__(self):
        self.instruction_counter = 0
        self.instructions = [
                            "look mirror", 
                            "get hairpin",
                            "unlock chest with hairpin",
                            "get hammer from chest",
                            "unlock door with hairpin",
                            "open door"]

    def connection_made(self, transport):
        self.transport = transport
        #self.transport.write("Hello World".encode())

    def data_received(self, data):
        text = data.decode()
        print(text)
        time.sleep(.2)
        if text == "SUBMIT autograde command:<EOL>\n":
            print("Client: submit request")
            self.transport.write("SUBMIT,Jaron Lee,jaron.lee@jhu.edu,9,1092".encode())
        if text.startswith("SUBMIT: OK"):
            test_id = text.split(",")[1]
            print("Client: success, {}".format(test_id))
        else:
            if self.instruction_counter < len(self.instructions):



                instruction = self.instructions[self.instruction_counter] + "<EOL>\n"
                print("Client: {}".format(instruction))
                self.transport.write(instruction.encode())
            else:
                print("RAN OUT OF INSTRUCTIONS!")



            

            
         

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(StudentClient,'192.168.200.52',19003)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    client.close()
    loop.run_until_complete(client.close())
    loop.close()
