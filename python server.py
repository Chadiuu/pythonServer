import socket
import os
from mss import mss
from datetime import datetime
import keyboard

class Control:
    def handle_command(self, command):
        raise NotImplementedError("This method should be implemented by subclasses")


class MediaControl(Control):
    def handle_command(self, command):
        if command == "Pause":
            return self.pause()
        elif command == "Next":
            return self.next_track()
        elif command == "Previous":
            return self.previous_track()
        else:
            return "Unknown Media Command"

    def pause(self):
        keyboard.send("play/pause media")
        return "play/pause"


    def next_track(self):
        keyboard.send("next track")
        return "next track"


    def previous_track(self):
        keyboard.send("previous track")
        return "next previous track"
    



class VolumeControl(Control):
    def handle_command(self, command):
        if command == "Volume Up":
            return self.volume_up()
        elif command == "Volume Down":
            return self.volume_down()
        elif command == "Mute":
            return self.mute()
        else:
            return "Unknown Volume Command"

    def volume_up(self):
        keyboard.send("volume up")
        return "volume increased"


    def volume_down(self):
        keyboard.send("volume down")
        return "volume decreased"


    def mute(self):
        keyboard.send("volume mute")
        return "volume muted"



class GeneralControl(Control):
    def handle_command(self, command):
        if command == "Screenshot":
            return self.screenshot_action()
        elif command == "Sleep":
            return self.sleepPC()
        elif command == "Lock PC":
            return self.lockPC()
        else:
            return "Unknown General Command"

    def screenshot_action(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        file_path = os.path.join(desktop_path, filename)
        with mss() as sct:
            sct.shot(output=file_path)
        
        print(f"Screenshot saved to {file_path}")
        return file_path


    def sleepPC(self):
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
        return "sleep PC"

    def lockPC(self):
        os.system('rundll32.exe user32.dll,LockWorkStation')
        return "lockPC"


class Server:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.media_control = MediaControl()
        self.volume_control = VolumeControl()
        self.general_control = GeneralControl()

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
                        print(f"Received: {data}")
                        response = self.route_command(data)
                        conn.sendall(response.encode())

    def route_command(self, command):
        if command in ["Pause", "Next", "Previous"]:
            return self.media_control.handle_command(command)
        elif command in ["Volume Up", "Volume Down", "Mute"]:
            return self.volume_control.handle_command(command)
        elif command in ["Sleep", "Lock PC", "Screenshot"]:
            return self.general_control.handle_command(command)
        else:
            return "Unknown Command"
if __name__ == "__main__":
    server = Server()
    server.start()





# def stop_media():
#     keyboard.send("stop media")
# def sleepComputer():
#     os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
#     return True
# import os
# from mss import mss
# from datetime import datetime

# def take_screenshot():
#     # Get the path to the Desktop
#     desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
#     # Generate a unique filename using the current timestamp
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"screenshot_{timestamp}.png"
    
#     # Full path to save the screenshot
#     file_path = os.path.join(desktop_path, filename)
    
#     # Take the screenshot and save it to the Desktop
#     with mss() as sct:
#         sct.shot(output=file_path)
    
#     print(f"Screenshot saved to {file_path}")
#     return file_path


# def lockPc():
#     os.system('rundll32.exe user32.dll,LockWorkStation')
#     return True
# def shutdownpc():
#     os.system('shutdown /s /t 1')
