import playground
import asyncio
import sys

def partial(result):
    class StudentClient(asyncio.Protocol):
        def __init__(self):
            self.result = result
            pass

        def connection_made(self, transport):
            self.transport = transport
            self.transport.write("<EOL>\n".encode())
            print(self.result)
            #self.transport.write("Hello World".encode())

        def data_received(self, data):
            text = data.decode()
            print("CR: ", text)
            time.sleep(.2)
            if text == "SUBMIT autograde command:<EOL>\n":
                print("C: submit request")
                self.transport.write("RESULT,{}<EOL>\n".format(self.result).encode())

    return StudentClient


if __name__ == "__main__":
    result = sys.argv[1]
    
    loop = asyncio.get_event_loop()
    coro = playground.create_connection(partial(result),'20194.0.0.19000',19005)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    client.close()
    loop.run_until_complete(client.close())
    loop.close()
