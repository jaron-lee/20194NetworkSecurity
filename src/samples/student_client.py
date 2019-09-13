import asyncio

class StudentClient(asyncio.Protocol):
    def __init__(self):
        pass

    def connection_made(self, transport):
        self.transport = transport
        #self.transport.write("Hello World".encode())

    def data_received(self, data):
        text = data.decode()
        print(text)
        if text == "SUBMIT autograde command:<EOL>\n":
            print("Client: submit request")
            self.transport.write("SUBMIT,Jaron Lee,jaron.lee@jhu.edu,9,1092")
         

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
