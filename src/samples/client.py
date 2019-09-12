import socket
import time

def send_recv_instruction(s, message):
    message = message + "\n"
    s.send(message.encode())
    time.sleep(0.25)
    data = s.recv(1024)
    print(data.decode())

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
        data = s.recv(1024).decode()
        time.sleep(.25)
        print(data)
        s.send("Jaron Lee".encode())

        for message in messages:
            send_recv_instruction(s, message)


if __name__ == "__main__":
    main()

