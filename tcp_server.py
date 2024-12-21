import socket

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                # Обработка команд
                command = data.decode().strip()
                if command.startswith("SET"):
                    # Обработка команды SET
                    print(f"Setting value: {command}")
                elif command.startswith("GET"):
                    # Обработка команды GET
                    print(f"Getting value: {command}")
                    conn.sendall(b"Value: 10\n")
                elif command == "READ_ALL":
                    # Обработка команды READ_ALL
                    print("Sending all values")
                    conn.sendall(b"Block1.Input1: 10\nBlock2.Input2: 10\n")

if __name__ == "__main__":
    start_server("localhost", 12345)