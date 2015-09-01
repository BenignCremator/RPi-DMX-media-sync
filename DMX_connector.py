#!/usr/bin/python

import sys
import os.path
import logging
from pygame import mixer, time, event

from ola.ClientWrapper import ClientWrapper

if len(sys.argv > 1):
    for arg in range(len(sys.argv[1:])):
        if sys.argv[arg] == "-f" or arg == "--cfgfile":
            cfg_file = sys.argv[arg + 1]
            arg = arg + 1
        if sys.argv[arg] == "-d" or arg == "--cfgdir":
            cfg_dir = sys.argv[arg + 1]
            arg = arg + 1

if cfg_file == '':
    cfg_file='/home/olad/dmx_connector.py'
if cfg_dir == '':
    tmp_dir, cfg_file = os.path.split(cfg_file)
    if tmp_dir:
        cfg_dir = tmp_dir
        del tmp_dir
    else:
        cfg_dir = '/home/olad'
else:
    mesg = 'Config file '+cfg_file+' missing.  Create config file before running.'
    raise ImportError(mesg)

def NewData(data):
  #print data
  for addr in addresses:
      New Values[addr] = data[addr-1]

def read_playlist(root_dir, playlist):
    '''
    Checks if playlist is within the appropriate directory, and them imports and returns
    its contents to be loaded into the calling player.
    '''


def file_import(fileName, filePath = ''):
    '''
    Check path and file, imports file and returns objects.
    '''
    if os.path.isfile(filePath+'/'+fileName):
        if fileName[-3:] == '.py':
            sys_path=sys.path
            sys.path=[filePath]
            exec('import '+fileName[:-3])
            exec('fileName ='+fileName[:-3])
            sys.path=sys_path
            return fileName
        else:
            mesg = 'Configuration file '+fileName+' is not properly formatted.'\
                +'  Check and redit.'
            raise ImportError(mesg)
    else:
        mesg = 'Configuration file '+fileName+' is missing.  Create'\
            +' configuration file or specify correct location.'
        raise ImportError(mesg)

class SoundPlayer(object):
    def __init__(self):
        logging.basicConfig(filename='SoundPlayer.log', level=logging.DEBUG)
        mixer.init()
        mixer.set_num_channels(8)
        self.audio_root = "../../sound_effects/animals"
        self.playlist = read_playlist(self.audio_root)
        self.sounds = {}
        

    def load(self, sound_id):
        if sound_id in self.sounds.keys():
            logging.debug("Tried to load same sound twice. sound_id= %d", sound_id)
            return
        self.sounds[sound_id] = mixer.Sound(self.audio_root+"/"+self.playlist[sound_id])
        
    def play(self, sound_id):
        if sound_id not in self.sounds.keys():
            logging.debug("Tried to play before loading. sound_id= %d", sound_id)
            self.load(sound_id)
        self.sounds[sound_id].play()            
            
    def stop(self, sound_id):
        if sound_id not in self.sounds.keys():
            logging.debug("Tried to stop unloaded sound. sound_id= %d", sound_id)
            self.load(sound_id)
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

config = file_import(cfg_file, dfg_dir)
wrapper = ClientWrapper()
client = wrapper.Client()
client.RegisterUniverse(universe, client.REGISTER, NewData)
wrapper.Run()

