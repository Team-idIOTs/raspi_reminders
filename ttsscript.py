import sys
from gtts import gTTS
import subprocess


tts_str = ''
task_name = sys.argv[1]
for i in range(2, len(sys.argv)):
    tts_str += sys.argv[i] + " "

tts = gTTS(tts_str)
tts.save(task_name + ".mp3")
subprocess.call(['omxplayer', task_name + ".mp3"])
