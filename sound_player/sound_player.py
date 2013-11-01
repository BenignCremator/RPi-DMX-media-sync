import sys
import os.path
from pygame import mixer, time

def read_playlist(root_dir):
    playlist = [s.strip() for s in open(root_dir+"/playlist").readlines()]
    playlist.remove('playlist')
    return playlist



class SoundPlayer(object):
    def __init__(self):
        mixer.init()
        mixer.set_num_channels(8)
        self.audio_root = "sound_effects/animals"
        self.playlist = read_playlist(self.audio_root)
        self.sounds = {}

    def load(self, sound_id):
        self.sounds[sound_id] = mixer.Sound(self.audio_root+"/"+self.playlist[sound_id])
        
    def play(self, sound_id):
            self.sounds[sound_id].play()
            
            
    def stop(self, sound_id):
        self.sounds[sound_id].stop()


def test_loop():
    '''Simple keyboard-driven controller for testing'''
    sp = SoundPlayer()
    print("Enter symbol and number. Symbol is one of l (load), + (play), - (stop). Number is index of a sound")
    print("Example: l4 to load 5th sound in the playlist, +4 to play it. Remember to load first!")
    actions = {}
    actions ["l"] = sp.load
    actions ["+"] = sp.play
    actions ["-"] = sp.stop


    while True:
        action = raw_input("l,+,-")
        actions[action[0]](int(action[1:]))
    

def test():
    sp = SoundPlayer()
    for i in range(8):
        sp.load(i)
    t = sp.sounds[1].get_length()*1000
    sp.play(1)
    time.wait(t)
#    while sp.sounds[1].get_busy():
#        time.wait(500)

