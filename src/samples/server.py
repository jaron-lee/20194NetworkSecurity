import socket
from escape_room_001 import *
import functools

def write_function(string, conn):
    conn.send(string.encode())

def main():
    HOST = ""
    PORT = 50006
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print("Server launched on {}".format(PORT))
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            enquiry = "What is your name?"
            conn.send(enquiry.encode())
            name = conn.recv(1024).decode()
            print("Thanks {}".format(name))

            while True:
                game = EscapeRoomGame(output=functools.partial(write_function, conn=conn))
                game.create_game()
                game.start()
                while game.status == "playing":
                    data = conn.recv(1024)
                    data_as_string = data.decode()
                    lines = data_as_string.split("\n")
                    for line in lines:
                        if len(line) > 0:
                            print(line)
                            output = game.command(line)

if __name__ == "__main__":
    main()
