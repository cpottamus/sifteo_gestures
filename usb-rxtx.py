#!/usr/bin/env python

#
# Simple PyUSB demo to interact with the Sifteo SDK USB example.
#

import usb # expects PyUSB (http://pyusb.sourceforge.net) to be installed
import sys
import time
from scripts import * 


SIFTEO_VID  = 0x22fa
BASE_PID    = 0x0105

IN_EP       = 0x81
OUT_EP      = 0x01
INTF        = 0x0
MAX_PACKET  = 64

USER_SUBSYS = 7

CURR_APP = currApp()

CLICK_LATENCY_MAX = .15 #latency difference between registering 1 and 2 clicks

# Cube 1
TOUCH_START = 0 #Start Time of Touch
IS_TOUCHING = 0 #Touch prevstate Flag
IS_SHAKING = 0 #Shaking prevstate Flag
IS_TILTING_X = 0 #Tilting X prevstate Flag
IS_TILTING_Y = 0 #Tilting Y prevstate Flag
LAST_TAP_TIME = 0 #Time of last tap
JUST_TAPPED = 0 #Flag for initial touch (to determine if there is a second touch in time)
IS_LONG_TOUCHING = 0 #long touch flag

# Cube 2
TOUCH_START_1 = 0 #Start Time of Touch
IS_TOUCHING_1 = 0 #Touch prevstate Flag
IS_SHAKING_1 = 0 #Shaking prevstate Flag
IS_TILTING_X_1 = 0 #Tilting X prevstate Flag
IS_TILTING_Y_1 = 0 #Tilting Y prevstate Flag
LAST_TAP_TIME_1 = 0 #Time of last tap
JUST_TAPPED_1 = 0 #Flag for initial touch (to determine if there is a second touch in time)
IS_LONG_TOUCHING_1 = 0 #long touch flag

def find_and_open():
    dev = usb.core.find(idVendor = SIFTEO_VID, idProduct = BASE_PID)
    if dev is None:
        sys.stderr.write('Device is not connected\n')
        sys.exit(1)

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    return dev

def send(dev, bytes, timeout = 1000):
    """
    Write a byte array to the device.
    """

    # Ensure that our message will be dispatched appropriately by the base.
    # Highest 4 bits specify the subsystem, user subsystem is 7.
    USER_HDR = USER_SUBSYS << 4
    
    #WRITE HERE
    msg = [1, 25, 30, USER_HDR]
    
    msg.extend(bytes)

    #print 'msg :: ', msg
    #print 'msgbytes :: ', msg.extend(bytes)

    if len(msg) > MAX_PACKET:
        raise ValueError("msg is too long")

    return dev.write(OUT_EP, msg, INTF, timeout)

def receive(dev, timeout=500):
    """
    Read a byte array from the device.
    """
    try:
        # catch timeouts, and just return empty a byte array
        msg = dev.read(IN_EP, MAX_PACKET, INTF, timeout)
    except usb.core.USBError:
        return -1, []

    if len(msg) < 4:
        return -1, []

    subsystem = (msg[3] & 0xff) >> 4
    if subsystem != USER_SUBSYS:
        return -1, []

    return type, msg[4:]

dev = find_and_open()
b = 0
while True:
    msg = [b]
    b = (b + 1) % 100
    send(dev, msg)

    type, payload = receive(dev)    
    if len(payload) >= 7:
        ax = payload[0]
        ay = payload[1]
        az = payload[2]
        tx = payload[3]
        ty = payload[4]
        tz = payload[5]
        tch = payload[6]
        shk = payload[7]

    if len(payload) >= 15:
        ax1 = payload[8]
        ay1 = payload[9]
        az1 = payload[10]
        tx1 = payload[11]
        ty1 = payload[12]   
        tz1 = payload[13]
        tch1 = payload[14]
        shk1 = payload[15]


########## TOUCH #############
    #Single tap time timer flag
    if JUST_TAPPED and time.time() - LAST_TAP_TIME >= CLICK_LATENCY_MAX:
        playPause()
        JUST_TAPPED = 0

    #If touched and not touching before
    if tch and not tch == IS_TOUCHING:
        #start timer for holding interval
        TOUCH_START = time.time()
    #If a short touch
    if not tch and IS_TOUCHING and time.time() - TOUCH_START < .3:
        
        #set single tap flag
        JUST_TAPPED = 1

        #double Tap touch
        if time.time() - LAST_TAP_TIME < CLICK_LATENCY_MAX:
            dialog()
            JUST_TAPPED = 0  

        LAST_TAP_TIME = time.time()
    #If long touch
    if tch and time.time() - TOUCH_START >= .3:
        keyDownCommand()
        IS_LONG_TOUCHING = 1

    #Just finished long touch
    if not tch and IS_LONG_TOUCHING:
        keyUpCommand()
        IS_LONG_TOUCHING = 0
        CURR_APP = currApp()
    #If a long touch and tx tilt
    if tch and time.time() - TOUCH_START >= .3 and not tx == IS_TILTING_X:
        #if right tilt
        if tx == 1:
            nextApplication()
        #if left tilt
        if tx == 255:
            prevApplication()

    #If a long touch and ty tilt
    if tch and time.time() - TOUCH_START >= .3 and not ty == IS_TILTING_Y:
        #if up tilt
        if tx == 1:
            volumeUp()
        #if down tilt
        if tx == 255:
            volumeDown()


########## Shake #############
    if shk and not shk == IS_SHAKING:
        # dialog()
        pass

########## Accel #############



########## Update Variables #############

    IS_TOUCHING = tch
    IS_TILTING_X = tx    
    IS_TILTING_Y = ty
    IS_SHAKING = shk
        
########## Cube 2 #############
    if CURR_APP == 'iTunes':
        ########## TAP #############

        # If tapped and not touching before
        if tch1 and not IS_TOUCHING_1:
            # Start timer for holding interval
            TOUCH_START_1 = time.time()
            IS_TOUCHING_1 = True
        
        # If a short tap (just removed finger and the tap was short)
        if not tch1 and IS_TOUCHING_1 and time.time() - TOUCH_START_1 < .3:

            # Set tap flag
            JUST_TAPPED_1 = 1

            # Detect double tap (this tap came almost immediately after last tap)
            if time.time() - LAST_TAP_TIME_1 < CLICK_LATENCY_MAX:
                shuffle()
                JUST_TAPPED_1 = 0  

            LAST_TAP_TIME_1 = time.time()

        # If a single tap (just tapped and enough time has passed for it to not be a double tap)
        if JUST_TAPPED_1 and time.time() - LAST_TAP_TIME_1 >= CLICK_LATENCY_MAX:
            playPause()
            JUST_TAPPED_1 = 0

        # If long touch (still holding down and have been for awhile)
        if tch1 and time.time() - TOUCH_START_1 >= .3:
            IS_LONG_TOUCHING_1 = 1        

        # Just finished long touch
        if not tch1 and IS_LONG_TOUCHING_1:
            IS_LONG_TOUCHING_1 = 0        

        ########## TILT #############     

        # Currently long touching and new tx tilt
        if IS_LONG_TOUCHING_1 and tx1 and not IS_TILTING_X_1:

            # If right tilt
            if tx1 == 1:
                nextTrack()
            # If left tilt
            if tx1 == 255:
                prevTrack()

        # Currently long touching and new ty tilt
        if IS_LONG_TOUCHING_1 and ty1 and not IS_TILTING_Y_1:

            # If up tilt
            if ty1 == 1:
                volumeDown()
            # If down tilt
            if ty1 == 255:
                volumeUp()

        ########## SHAKE #############

        # Currently long touching and new shake (GETS CONFUSED WITH LONG TOUCH AND TILT)
        if IS_LONG_TOUCHING_1 and shk1 and not IS_SHAKING_1:
            shuffle()            

        ########## UPDATE VARIABLES #############  
        IS_TOUCHING_1 = tch1
        IS_TILTING_X_1 = tx1
        IS_TILTING_Y_1 = ty1
        IS_SHAKING_1 = shk1