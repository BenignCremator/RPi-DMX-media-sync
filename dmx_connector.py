###  Raspberry Pi DMX Media Player master config file
###  Import this to configure the player
###      It imports its children for further configurations

#  The DMX universe the unit responds to over ArtNET or other DOE
universe = 1

#  Locations of child config files, playlists, and media
audio_media = "~/media/video"
auido_playlist_index = "~/playlists/audio_index.py"
video_media = "~/media/video"
video_playlist_index = "~/playlists/video_index.py"

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

audio_controls = 30
audio_vol = 31
audio_pan = 32
