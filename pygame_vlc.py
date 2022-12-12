import pygame
from pygame.locals import *
import vlc

# Define files to play
sound_files = ['sounds/SeptemberGrooveTest.wav',
               'sounds/TwoSeconds.wav',
               ]

instances = [] # Empty list for vlc player instances
medias = []    # Empty list for 
players = []

# Set up vlc with each sound in a seperate player within a seperate instance
for idx, file in enumerate(sound_files):
    print("Loading",file)
    instances.append(vlc.Instance())              # Create new instance
    medias.append(instances[idx].media_new(file)) # Load media file to instance
    players.append(vlc.MediaPlayer())             # Create players
    players[idx].set_media(medias[idx])           # Add instance to player

pygame.init()             # Initialise pygame
pygame.display.set_mode() # Initialise display window   

# This was to avoid vlc overwriting imputs from pygame but isn't needed
for player in players:
    player.video_set_mouse_input(False)
    player.video_set_key_input(False)

length = players[1].get_length()
players[1].play() # Play song (not currently in loop but can be)

while True: # Infinite loop
    for event in pygame.event.get():  # For any event (i.e. key press)
        if event.type == pygame.QUIT: # if event is a quit event, (i.e. alt-F4)
            pygame.quit()             # quit game
            for player in players:    # and for each sound player
                player.stop()         # stop it.
        if event.type == pygame.KEYDOWN:   # If a key is pressed
            if event.key == pygame.K_d:    # and the key is d,
                print(length-players[1].get_time())
                players[1].stop()          # stop any previous playback
                players[1].play()          # then play test sound.
            if event.key == pygame.K_s:    # If the key is s,
                players[0].stop()          # Stop any previous playback
                players[0].play()          # and restart the song.
        pygame.display.update()            # Update display (resets loop)

