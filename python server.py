import os
import socket
from datetime import datetime
from mss import mss
import keyboard


class Control:
    def handle_command(self, command):
        raise NotImplementedError("This method should be implemented by subclasses")


class MediaControl(Control):
    def __init__(self):
        self.commands = {
            1: self.pause,
            2: self.next_track,
            3: self.previous_track,
        }

    def handle_command(self, command):
        action = self.commands.get(command)
        if action:
            return action()
        return "Unknown Media Command"

    def pause(self):
        keyboard.send("play/pause media")
        return "Media Paused/Played"

    def next_track(self):
        keyboard.send("next track")
        return "Next Track"

    def previous_track(self):
        keyboard.send("previous track")
        return "Previous Track"


class VolumeControl(Control):
    def __init__(self):
        self.commands = {
            4: self.volume_up,
            5: self.volume_down,
            6: self.mute,
        }

    def handle_command(self, command):
        action = self.commands.get(command)
        if action:
            return action()
        return "Unknown Volume Command"

    def volume_up(self):
        keyboard.send("volume up")
        return "Volume Increased"

    def volume_down(self):
        keyboard.send("volume down")
        return "Volume Decreased"

    def mute(self):
        keyboard.send("volume mute")
        return "Volume Muted"


class GeneralControl(Control):
    def __init__(self):
        self.commands = {
            7: self.screenshot_action,
            8: self.sleep_pc,
            9: self.lock_pc,
        }

    def handle_command(self, command):
        action = self.commands.get(command)
        if action:
            return action()
        return "Unknown General Command"

    def screenshot_action(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        file_path = os.path.join(desktop_path, filename)
        with mss() as sct:
            sct.shot(output=file_path)
        print(f"Screenshot saved to {file_path}")
        return f"Screenshot saved: {file_path}"

    def sleep_pc(self):
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        return "PC is now sleeping"

    def lock_pc(self):
        os.system('rundll32.exe user32.dll,LockWorkStation')
        return "PC Locked"


class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.media_control = MediaControl()
        self.volume_control = VolumeControl()
        self.general_control = GeneralControl()

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
