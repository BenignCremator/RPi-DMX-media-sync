###  Raspberry Pi DMX Media Player master config file
###  Import this to configure the player
###      It imports its children for further configurations

#  The DMX universe the unit responds to over ArtNET or other DOE
universe = 1

#  Locations of child config files, playlists, and media
audio_media = "/media/video"
auido_playlist_index = "/playlists/audio_index.py"
video_media = "/media/video"
video_playlist_index = "/playlists/video_index.py"

#  Hope many audio players to initialize, read docs on audio
#  performace and number of players in use
audio_players = 8

#  True to initialize video player, False to not initialize it
video_player = True

#  Set addresses in config files, or (False) sequentially
addressing = True

#  Base DMX address is addressing is sequential
base_address = 21

#  DMX addresses of video player
video_load_playlist = 22
video_select_file  = 23
video_controls = 24
video_vol = 25
video_pan = 26

#  Addresses to manage audio players
audio_player_select = 27
audio_load_playlist = 28
audio_select_file = 29

#  Addresses of audio players
audio_player = 0
audio_controls = 30
audio_vol = 31
audio_pan = 32

audio_player = 1
audio_controls = 33
audio_vol = 34
audio_pan = 35

audio_player = 2
audio_controls = 36
audio_vol = 37
audio_pan = 38

audio_player = 3
audio_controls = 39
audio_vol = 40
audio_pan = 41

audio_player = 4
audio_controls = 42
audio_vol = 43
audio_pan = 44

audio_player = 5
audio_controls = 45
audio_vol = 46
audio_pan = 47

audio_player = 6
audio_controls = 48
audio_vol = 49
audio_pan = 50

audio_player = 7
audio_controls = 51
audio_vol = 52
audio_pan = 53


