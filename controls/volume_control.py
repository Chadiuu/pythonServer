from controls.control import Control
import keyboard

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
