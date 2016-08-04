import subprocess
import time

osa = "osascript"
lb = '-e'

'''
Causes the screen to sleep, which will also lock if your settings
are set appropriately (they should be anyway, set them that way)
'''
def sleep_mac_display():
    subprocess.call('pmset displaysleepnow', shell=True)


'''
Toggles pause/play for spotify



'''
def touchless():
	line4= 'activate application "Safari"'
	# line3= 'repeat 10 times'
	line5= 'tell application "System Events" to keystroke "Down Arrow"'
	line6 = 'end repeat'
	subprocess.call([osa, lb, line4, lb, line5, lb, line6])


def toggle_spotify():
    line1 = 'tell application "Spotify"'
    line2 = 'playpause'
    line3 = 'end tell'
    subprocess.call([osa, lb, line1, lb, line2, lb, line3])

'''
Best executed via command line with the & argument following it
Example: python -c "from actions import grief_poor_user; grief_poor_user(3)" &
Then close the terminal and they will suffer
'''
def grief_poor_user(x):
    while True:
        time.sleep(x)
        toggle_spotify()





