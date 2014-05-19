#!/bin/bash

osascript -e 'if is_running("iTunes") then
    tell application "iTunes"
        playpause
    end tell
else
    tell application "Spotify"
        playpause
    end tell end if'
 