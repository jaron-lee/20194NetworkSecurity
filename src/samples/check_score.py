import socket
import sys

def main(args):
    HOST = "192.168.200.52"
    PORT = int(args[0])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024).decode()
        s.send("RESULT,{}".format(args[1]).encode())
        data = s.recv(1024).decode()
        print(data)

if __name__ == "__main__":
    main(sys.argv)
