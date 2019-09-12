import socket
import time
from escape_room_001 import *
import functools 

def write_function(string, conn):
    conn.send(string.encode())

def send_recv_instruction(s, message):
    message = message + "\n"
    s.send(message.encode())
    time.sleep(0.25)
    data = s.recv(1024)
    print(data.decode())

def get_data(s):
    data = s.recv(1024).decode()
    print(data)
    return data

def main():
    HOST = "192.168.200.52"
    PORT = 19002
    messages = ["look mirror", 
            "get hairpin", 
            "unlock door with hairpin",
            "open door"]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected")
        time.sleep(.25)
        print(get_data(s))
        s.send("Jaron Lee".encode())
        get_data(s)


        for message in messages:
            send_recv_instruction(s, message)

        time.sleep(0.25)

        get_data(s)
        game = EscapeRoomGame(output=functools.partial(write_function, conn=conn))
        game.create_game()
        game.start()
        while game.status == "playing":
            data = get_data(s)
            lines = data_as_string.split("\n")
            for line in lines:
                output = game.command(line)

            s.send(output.encode())


if __name__ == "__main__":
    main()

