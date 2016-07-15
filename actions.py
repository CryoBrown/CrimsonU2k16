import subprocess

'''
Causes the screen to sleep, which will also lock if your settings
are set appropriately (they should be anyway, set them that way)
'''
def sleep_mac_display():
    subprocess.call('pmset displaysleepnow', shell=True)
