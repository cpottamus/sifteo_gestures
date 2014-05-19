from applescript import AppleScript

def playPause():
    scpt = AppleScript('''
        tell application "iTunes"
            playpause
        end tell
    ''')
    scpt.run()

def minimize():
	scpt = AppleScript('''
		set activeApp to name of (info for (path to frontmost application))
		
			tell application activeApp
				set miniaturized of every window to true
			end tell
		
		
				tell application "Terminal"
					set minimized of every window to true
				end tell
					

	''')
	scpt2 = AppleScript('''
		tell application (path to frontmost application as text)	
			set miniaturized of (get window 1) to true
		end tell
	''')
	print(scpt2.run())

def dialog():
	scpt = AppleScript('''
		tell application (path to frontmost application as text)
			display dialog "Possible motions:\nTilt, Shake, Move, Tap"
		end tell
	''')
	scpt.run()

def nextApplication():
	scpt = AppleScript('''
		tell application "System Events"
			keystroke tab using {command down}
		end tell
	''')
	scpt.run()

def prevApplication():
	scpt = AppleScript('''
		tell application "System Events"
			keystroke tab using {command down, shift down}
		end tell
	''')
	scpt.run()


