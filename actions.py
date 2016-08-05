import subprocess
import time
import os

osa = "osascript"
lb = '-e'
FNULL = open(os.devnull, 'w')

'''
Causes the screen to sleep, which will also lock if your settings
are set appropriately (they should be anyway, set them that way)
'''
def sleep_mac_display():
    subprocess.call(['pmset', 'displaysleepnow'])

'''
Right arrow key press event
'''
def touchless_right():
    line1= 'tell application "System Events" to key code 124'
    subprocess.call([osa, lb, line1])
'''
Left arrow key press event
'''
def touchless_left():
    line1= 'tell application "System Events" to key code 123'
    subprocess.call([osa, lb, line1])

'''
Toggles pause/play for spotify
'''
def toggle_play():
    line1 = 'tell application "System Events" to key code 100'
    subprocess.call([osa, lb, line1])

'''
Plays the volume change sound
'''
def volume_sound():
    subprocess.call(["afplay", "/System/Library/LoginPlugins/BezelServices.loginPlugin/Contents/Resources/volume.aiff"], 
        stdout=FNULL, stderr=FNULL)

'''
Increases volume
'''
def volume_up():
    vol_plus = "set volume output volume (output volume of (get volume settings) + 6)"
    subprocess.call([osa, lb, vol_plus])
    volume_sound()

'''
Decreases volume
'''
def volume_down():
    vol_minus = "set volume output volume (output volume of (get volume settings) - 6)"
    subprocess.call([osa, lb, vol_minus])
    volume_sound()


'''
Best executed via command line with the & argument following it
Example: python -c "from actions import grief_poor_user; grief_poor_user(3)" &
Then close the terminal and they will suffer
'''
def grief_poor_user(x):
    while True:
        time.sleep(x)
        toggle_play()





