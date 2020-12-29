import os
#Hide pygame prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer
import time
import threading

SOUNDFILE = '/home/rak3sh/stocks/sounds/announcer_kill_ultra_01.wav'

def _play():
    # Starting the mixer 
    mixer.init() 
    
    # Loading the song 
    mixer.music.load(SOUNDFILE) 
    
    # Setting the volume 
    mixer.music.set_volume(0.7) 
    
    # Start playing the song 
    mixer.music.play()
    time.sleep(3)

def play():
    x = threading.Thread(target=_play)
    x.start()
if __name__ == "__main__":
    play()
    time.sleep(1)
    play()

