# importing vlc module
import vlc
  
# importing time module
import time
  
  
# creating Instance class object
player = vlc.Instance()
  
# creating a new media list
media_list = player.media_list_new()
  
# creating a media player object
media_player = player.media_list_player_new()
  
# creating a new media
media = player.media_new('sounds/TwoSeconds.wav')
  
# adding media to media list
media_list.add_media(media)
  
# setting media list to the mediaplayer
media_player.set_media_list(media_list)
  
# setting loop
print(player.vlm_set_loop('sounds/TwoSeconds', True))
  
  
# start playing video
media_player.play()
  

# files = [{'file':'sounds/TwoSeconds.wav','length':1.4}]
# test = files[0]
#   
# # creating vlc media player object
# media_player = vlc.MediaPlayer()
# media = vlc.Media(test['file'])
# media_player.set_media(media)
# 
# while True:
#     media_player.play()
#     time.sleep(test['length'])
#     print(media_player.get_length()/1000-1) 
#     time.sleep(media_player.get_length()/1000-1)

# repeat = True
# 
# # printing value
# while repeat:
#     time.sleep(test['length'])
#     media_player.set_position(0)

