import os, sys, thread, time
sys.path.insert(0,"/Users/brownch/proj/LeapSDK/lib")
import Leap

import actions

class JustureListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def __init__(self, framestore, ticks):
        Leap.Listener.__init__(self)
        self.l_win = JustureWindow(framestore)
        self.r_win = JustureWindow(framestore)
        self.tock = 0
        self.ticks = ticks

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
        #Check if this frame matters and if so use it
        if self.tock == 0:
            self.per_tick(frame)
        self.tock = (self.tock+1)%self.ticks

    def per_tick(self, frame):
        #perform calculations per tick

        # Get hands
        for hand in frame.hands:

            if hand.is_left:
                print "LH"
                win = self.l_win
            else:
                print "RH"
                win = self.r_win
            print "-------------"
            win.push(hand)

            cur = win.extended_tuple(hand)
            num = win.int_tuple(cur)

            print("Extended: %s", num)
            print("Avg: %s", win.ext_average)


            if cur == tuple([True, True, True, True, True]):
                if win.check_average(win.ext_average, tuple([0.9, 0.9, 0.9, 0.9, 0.9]), num):
                    actions.sleep_mac_display()
                pass
            elif cur == tuple([True, False, False, False, False]):
                if win.check_average(win.ext_average, tuple([0.8, 0.2, 0.2, 0.2, 0.2]), num):
                    self.volume_change(hand.fingers[0])
            elif cur == tuple([False, False, False, False, True]):
                if win.check_average(win.ext_average, tuple([0.2, 0.2, 0.2, 0.2, 0.8]), num):
                    self.volume_change(hand.fingers[4])
            elif cur == tuple([False, False, True, True, True]):
                if win.check_average(win.ext_average, tuple([0.2, 0.2, 0.8, 0.8, 0.8]), num):
                    actions.toggle_spotify()


        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def volume_change(self, finger):
        if finger.direction[0] < 0:
            actions.volume_down()
        else:
            actions.volume_up()



class JustureWindow():

    def __init__(self, capacity):
        self.capacity = capacity
        self.id = -1

    def reroll(self, capacity):
        self.queue = []
        self.space = capacity
        self.ext_average = tuple([0.0, 0.0, 0.0, 0.0, 0.0])

    #Add to the window (removing oldest if window is to size, updating average as needed)
    def push(self, hand):
        if(hand.id != self.id):
            self.id = hand.id
            self.reroll(self.capacity)
        self.queue.append(hand)
        if(self.space > 0):
            self.space -= 1
        else:
            self.update_average(self.queue.pop(0), subtract=True)
        self.update_average(hand)

    #Update the average of a window
    def update_average(self, hand, subtract=False):
        scale = -1 if subtract else 1

        hand_tuple = self.normalize_five_tuple(self.extended_tuple(hand))
        l = []
        #string  = str(self.ext_average) + ("-" if subtract else "+") + str(hand_tuple)
        for (a, b) in zip(self.ext_average, hand_tuple):
            l.append(self.round_float(a + (scale * b)))
        #print (string + "=" + str(l))
        self.ext_average = tuple(l)

    #Normalize a five_tuple with capacity as the denominator
    def normalize_five_tuple(self, tup):
        l = []
        for t in tup:
            l.append(float(t)/self.capacity)
        return tuple(l)

    #Get a boolean tuple of fingers extended
    def extended_tuple(self, hand):
        l = []
        fse = hand.fingers.extended()
        for finger in hand.fingers:
            l.append(finger in fse)
        return tuple(l)

    #Get integer of extended tuple
    def int_tuple(self, ext):
        l = []
        for f in ext:
            l.append(int(f))
        return tuple(l)

    def round_float(self, f):
        e = 0.01/self.capacity
        if(f < e):
            return 0
        elif(1-f < e):
            return 1
        else:
            return f

    def check_average(self, real, thresholds, expected):
        print "-----------"
        print real
        print thresholds
        print expected
        for (r, t, e) in zip(real, thresholds, expected):
            if (e == 0 and r > t):
                print str(r)
                print ">"
                print str(t)
                return False
            elif (e == 1 and r < t):
                print str(r)
                print "<"
                print str(t)
                return False
        return True

    def oldest(self):
        if len(self.queue) == 0:
            print "Nothing in the window"
            return None
        return self.queue[0]

    def newest(self):
        if len(self.queue) == 0:
            print "Nothing in the window"
            return None
        return self.queue[-1]



def main():
    # Create a sample listener and controller
    listener = JustureListener(50, 10)
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

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
