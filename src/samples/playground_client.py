import asyncio
import playground

class EchoClient(asyncio.Protocol):
    def __init__(self):
        pass

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write("<EOL>\n".encode())

    def data_received(self, data):
        print(data.decode() + "sent")

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    coro = playground.create_connection(EchoClient,'localhost',8080)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    client.close()
    loop.run_until_complete(client.close())
    loop.close()
