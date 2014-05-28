# -*- coding: utf-8 -*-
from applescript import AppleScript, AEType

####################################
##          System Level          ##
####################################

## Help dialog
def dialog():
	scpt = AppleScript('''
		tell application (path to frontmost application as text)
			display dialog "Possible motions:\nTilt, Shake, Move, Tap"
		end tell
	''')
	scpt.run()

## Window buttons
# Click one of the window bar buttons (close, minimize, or maximize)
def clickTopButton(buttonNum):
	scpt = AppleScript('''
		tell application "System Events" to tell (process 1 where frontmost is true)
		    click button ''' +  str(buttonNum) + ''' of window 1
		end tell
	''')
	scpt.run()

def close():
	clickTopButton(0)

def minimize():
	clickTopButton(3)

def maximize():
	clickTopButton(2)

# A 'purer' way to minimize a window; this however doesn't work for close/maximize
def minimize2():
	scpt = AppleScript('''
		tell application "System Events" to tell (process 1 where frontmost is true)
		    click menu item "Minimize" of menu 1 of menu bar item "Window" of menu bar 1
		end tell
	''')
	scpt.run()

## Move windows
# Base function for running expose-related shell scripts
def exposeShellScript(num):
	scpt = AppleScript('do shell script "/Applications/Utilities/Expose.app/Contents/MacOS/Expose ' + str(num) + '"')
	scpt.run()

# See all windows; this will also return to normal window mode when in expose/desktop mode
def expose():
	exposeShellScript(0)

# Move windows away to see desktop
def desktop():
	exposeShellScript(1)

## Application switching
def keyDownCommand():
	scpt = AppleScript('''
		tell application "System Events"
			key down command
		end tell
	''')
	scpt.run()

def nextApplication():
	scpt = AppleScript('''
		tell application "System Events"
			keystroke tab
		end tell
	''')
	scpt.run()
	playSoundEffect('Pop')

def prevApplication():
	scpt = AppleScript('''
		tell application "System Events"
			keystroke tab using {shift down}
		end tell
	''')
	scpt.run()
	playSoundEffect('Pop')

def keyUpCommand():
	scpt = AppleScript('''
		tell application "System Events"
			key up command
		end tell
	''')
	scpt.run()
	playSoundEffect('Blow')

## A string of the current app's name
def currApp():
	scpt = AppleScript('''
		return (info for (path to frontmost application))
	''')
	dict = scpt.run()
	return dict[AEType('dnam')]

## Play Sound Effect
def playSoundEffect(sound):
	scpt = AppleScript('''
		do shell script "afplay /System/Library/Sounds/''' + sound + '''.aiff"
	''')
	scpt.run()

## Volume functions
def volumeUp():
	scpt = AppleScript('''				
		set volOutput to output volume of (get volume settings)
	    set volume output volume (volOutput + 6.25)
	''')
	scpt.run()
	playVolumeSound()

def volumeDown():
	scpt = AppleScript('''				
		set volOutput to output volume of (get volume settings)
	    set volume output volume (volOutput - 6.25)
	''')
	scpt.run()
	playVolumeSound()

# Show notification (doesn't work)
def overlay():
	scpt = AppleScript('''		
		--on run {arg1, arg2}
		--	do shell script "osascript -e 'display notification arg1 with title arg2'"
		--end run
		on run {arg1, arg2}
            do shell script "arg1='HI'; arg2='YES';osascript -e 'display notification arg1 with title arg2'"
        end run
	''')
	scpt.run('Python', 'Calling')

def mute():
	scpt = AppleScript('''				
		set isMuted to output muted of (get volume settings)
	    set volume output muted (not isMuted)
	''')
	scpt.run()

# Trigger the volume sound (note: it's included in this directory because the one in the OS is too long and causes blocking)
def playVolumeSound():
	scpt = AppleScript('''
		do shell script "afplay volume.aiff"
	''')
	scpt.run()

####################################
##             Music              ##
####################################
## Basic tell iTunes something
def tellItunes(value):
	scpt = AppleScript('''
	    tell application "iTunes" to ''' + value
	)
	scpt.run()

## Control song
def playPause():
    tellItunes('playpause')
    playSoundEffect('Submarine')

def stop():
    tellItunes('stop')

def nextTrack():
    tellItunes('next track')
    playSoundEffect('Blow')

def prevTrack():
    tellItunes('previous track')
    playSoundEffect('Blow')

def shuffle():
	scpt = AppleScript('''
		tell application "System Events" 
			perform action "AXPress" of (first menu item of process "iTunes"'s menu bar 1's menu bar item "Controls"'s menu 1's menu item "Shuffle"'s menu 1 whose name ends with "Shuffle")
		end tell
	''')
	scpt.run()
	playSoundEffect('Purr')

####################################
##              Test              ##
####################################
# Delay for one second
def delay():
	scpt = AppleScript('''
		delay 1
	''')
	scpt.run()

# Show going to expose and going back
def demoExpose():
	expose()
	delay()
	expose()

# Show application switcher
def demoApplicationSwitching():
	keyDownCommand()
	nextApplication()
	delay()
	nextApplication()
	delay()
	prevApplication()
	delay()
	prevApplication()
	delay()
	keyUpCommand()