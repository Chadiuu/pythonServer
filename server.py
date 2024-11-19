import socket
from controls.media_control import MediaControl
from controls.volume_control import VolumeControl
from controls.general_control import GeneralControl


class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.media_control = MediaControl()
        self.volume_control = VolumeControl()
        self.general_control = GeneralControl()

        # Mapping of numeric commands to their corresponding controllers
        self.command_map = {
            1: self.media_control,
            2: self.media_control,
            3: self.media_control,
            4: self.volume_control,
            5: self.volume_control,
            6: self.volume_control,
            7: self.general_control,
            8: self.general_control,
            9: self.general_control,
        }

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}")
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024).decode()
                        if not data:
                            break
                        try:
                            command = int(data)  # Convert command to integer
                            print(f"Received Command: {command}")
                            response = self.route_command(command)
                        except ValueError:
                            response = "Invalid Command Format"
                        conn.sendall(response.encode())

    def route_command(self, command):
        control = self.command_map.get(command)
        if control:
            return control.handle_command(command)
        return "Unknown Command"


if __name__ == "__main__":
    server = Server()
    server.start()
