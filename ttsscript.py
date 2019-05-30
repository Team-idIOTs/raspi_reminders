import sys
import subprocess


tts_str = ''
task_name = sys.argv[1]
for i in range(2, len(sys.argv)):
    tts_str += sys.argv[i] + " "

subprocess.call(['omxplayer', task_name + ".mp3"])
