import subprocess
import applescript
import time

'''
Causes the screen to sleep, which will also lock if your settings
are set appropriately (they should be anyway, set them that way)
'''
def sleep_mac_display():
    subprocess.call('pmset displaysleepnow', shell=True)


script = applescript.AppleScript('''
    on run
        tell application "Spotify"
            set currentID to id of current track as string

            return currentID
        end tell
    end run
''')

def get_current_track():
    return script.run()

def save_current_track():
    track = get_current_track()


