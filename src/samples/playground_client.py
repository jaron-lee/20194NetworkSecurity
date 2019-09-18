import asyncio
import playground
import time

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
        self.transport.write("<EOL>\n".encode())
        #self.transport.write("Hello World".encode())

    def data_received(self, data):
        text = data.decode()
        print("CR: ", text)
        time.sleep(.2)
        if self.instruction_counter < len(self.instructions):
            if text == "SUBMIT autograde command:<EOL>\n":
                print("C: submit request")
                self.transport.write("SUBMIT,Jaron Lee,jaron.lee@jhu.edu,9,290<EOL>\n".encode())
            if text.startswith("SUBMIT: OK"):
                test_id = text.split(",")[1]
                print("C: success, {}".format(test_id))
            if self.instructions[self.instruction_counter] == "hit flyingkey with hammer":
                if text.split("<EOL>\n")[0].endswith("wall"):
                    instruction = self.instructions[self.instruction_counter] + "<EOL>\n"
                    self.transport.write(instruction.encode())
                    self.instruction_counter += 1
            else:
                instruction = self.instructions[self.instruction_counter] + "<EOL>\n"
                print("C: {}".format(instruction))
                self.transport.write(instruction.encode())
                self.instruction_counter += 1
        else:
            print("RAN OUT OF INSTRUCTIONS!")


         

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    coro = playground.create_connection(StudentClient,'20194.0.0.19000',19005)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    client.close()
    loop.run_until_complete(client.close())
    loop.close()
