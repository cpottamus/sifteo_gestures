# -*- coding: utf-8 -*-
from applescript import AppleScript, AEType
import os

####################################
##          System Level          ##
####################################

## Help dialog

def helpMenuMusic():
	scpt = AppleScript('''
		tell application (path to frontmost application as text)
			display dialog "Possible motions:\nTilt, Shake, Move, Tap"
		end tell
	''')
	scpt.run()

def helpMenuMouse():
	scpt = AppleScript('''
		tell application (path to frontmost application as text)
			display dialog "Possible motions:\nTilt, Shake, Move, Tap"
		end tell
	''')
	scpt.run()

def helpMenuEarth():
	scpt = AppleScript('''
		tell application (path to frontmost application as text)
			display dialog "Possible motions:\nTilt, Shake, Move, Tap"
		end tell
	''')
	scpt.run()

def helpMenuPaint():
	scpt = AppleScript('''
		tell application (path to frontmost application as text)
			display dialog "Possible motions:\nTilt, Shake, Move, Tap"
		end tell
	''')
	scpt.run()

def helpMenuChrome():
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
# Base function for running window-related commands
def windowCommand(keycode):
	scpt = AppleScript('tell application "System Events" to key code ' + str(keycode))
	scpt.run()

# See all windows
def expose():
	windowCommand(101)

# Move all windows to see desktop
def desktop():
	windowCommand(103)

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

# Trigger the volume sound (note: it's included in this directory because the one in the OS is too long and causes blocking)
def playVolumeSound():
	scpt = AppleScript('''
		do shell script "afplay volume.aiff"
	''')
	scpt.run()

# Show notification (doesn't work)
def overlay():
	scpt = AppleScript('''				
		display notification "HI SCOTT"
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

def fastFoward():
	tellItunes('set player position to (player position + 10)')

def rewind():
	tellItunes('set player position to (player position - 10)')

def shuffle():
	scpt = AppleScript('''
		tell application "System Events" 
			perform action "AXPress" of (first menu item of process "iTunes"'s menu bar 1's menu bar item "Controls"'s menu 1's menu item "Shuffle"'s menu 1 whose name ends with "Shuffle")
		end tell
	''')
	scpt.run()
	playSoundEffect('Purr')

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

def mute():
	scpt = AppleScript('''				
		set isMuted to output muted of (get volume settings)
	    set volume output muted (not isMuted)
	''')
	scpt.run()

####################################
##             Mouse              ##
####################################
def cliclick(argument):
	os.system('cliclick ' + argument)

def click():
	cliclick('c:.')

def move(xDiff, yDiff):
	cliclick('m:' + xDiff + ',' + yDiff)

####################################
##         Google Earth           ##
####################################
# Click in the console
def getInConsole():
	scpt = AppleScript('do shell script "cliclick c:20,700"')
	scpt.run()

# Click in Google Earth div
def getInEarth():
	scpt = AppleScript('do shell script "cliclick c:20,200"')
	scpt.run()

# Type
def typeIntoConsole(string):
	getInConsole()
	scpt = AppleScript('tell application "System Events" to keystroke "' + string + '"')
	scpt2 = AppleScript('tell application "System Events" to keystroke return')
	scpt.run()
	scpt2.run()

# Figure out on-screen coordinates for controls for direction
def getCoordsForDirection(direction):
	if direction == 'up':
		return '563,229'
	elif direction == 'left':
		return '548,246'
	elif direction == 'down':
		return '563,264'
	elif direction == 'right':
		return '580,246'

# Pan
def pan(direction):
	coords = getCoordsForDirection(direction)

	os.system('cliclick dd:' + coords)

def endPan(direction):
	os.system('cliclick du:.')

def zoomIn():
	typeIntoConsole('''
		var lookAt = ge.getView().copyAsLookAt(ge.ALTITUDE_RELATIVE_TO_GROUND);
		lookAt.setRange(lookAt.getRange() * 0.8);
		ge.getView().setAbstractView(lookAt);
	''')

def zoomOut():
	typeIntoConsole('''
			var lookAt = ge.getView().copyAsLookAt(ge.ALTITUDE_RELATIVE_TO_GROUND);
			lookAt.setRange(lookAt.getRange() * 1.2);
			ge.getView().setAbstractView(lookAt);
		''')

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

def demoVolume():
	volumeUp()
	volumeUp()
	volumeUp()
	volumeUp()
	volumeUp()
	volumeUp()
	volumeUp()
	volumeDown()
	volumeDown()
	volumeDown()
	volumeDown()
	volumeDown()
	volumeDown()
	volumeDown()

def demoPan():
	pan('down')
	delay()
	endPan('down')