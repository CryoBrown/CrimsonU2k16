import subprocess
import applescript
import time
import spotipy
import spotipy.util as util

'''
Causes the screen to sleep, which will also lock if your settings
are set appropriately (they should be anyway, set them that way)
'''
def sleep_mac_display():
    subprocess.call('pmset displaysleepnow', shell=True)


'''
Setup for spotify integration
'''

scope = 'user-library-modify'

script = applescript.AppleScript('''
    on run
        tell application "Spotify"
            set currentID to id of current track as string

            return currentID
        end tell
    end run
''')

cbspotify = 'spotify:user:12157124018'

scope = 'user-library-modify'

sp = None

def login_spotify(username):
    token = util.prompt_for_user_token(username, scope)
    global sp
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print "Can't get token for", username

def get_current_track():
    return script.run()

def save_current_track():
    if(sp == None):
        print("fuck")
        return False
    track = get_current_track()
    sp.current_user_saved_tracks_add([track])
    return True

login_spotify(cbspotify)
while True:
    raw_input('Enter to save...')
    save_current_track()






