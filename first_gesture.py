import os, sys, thread, time
sys.path.insert(0,'/Users/malhotrd/Documents/Leap/LeapSDK/lib')
import Leap
import subprocess

def sleep_mac_display():
    subprocess.call('pmset displaysleepnow', shell=True)

class JustureListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        L=[]

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            finger_extended = hand.fingers.extended()
            
            # Get fingers
            for finger in hand.fingers:
                
                
                    # if finger is True:
                    #     finger =1 
                    # else:
                    #     return 0    
                
                L.append(int(finger in finger_extended))
            print L
            # for x in range(frame.id)
            if L[0] ==0:
                if L[1]==0:
                    sleep_mac_display()
                    # print "True"
            # else:
            #     print "false"       






                # print "    %s finger, extended: %s" % (
                #     self.finger_names[finger.type],
                #     (finger in finger_extended))

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""


def main():
    # Create a sample listener and controller
    listener = JustureListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()