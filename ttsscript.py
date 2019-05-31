import vlc
import time
import sys
import subprocess

player = vlc.MediaPlayer(sys.argv[1] + ".mp3")
player.play()
time.sleep(10)
