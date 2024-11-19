from controls.control import Control
import keyboard

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
