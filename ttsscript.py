import sys
import subprocess

subprocess.call(['omxplayer', sys.argv[1] + ".mp3"])
