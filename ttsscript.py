import vlc
import time

player = vlc.MediaPlayer(sys.argv[1] + ".mp3")
player.play()
time.sleep(1)
