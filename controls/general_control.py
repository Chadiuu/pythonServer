from controls.control import Control
import os
from datetime import datetime
from mss import mss

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
