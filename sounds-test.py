import pygame
import wave
from pygame.locals import *
import os
import sounddevice
import vlc

# Define files to play
song_dir = 'sounds/Earth, Wind & Fire - September (Official HD Video).wav'
ding_dir = 'sounds/FourChannelTest.wav'

# Use wave to findout the framerate of the song
song_wav = wave.open(song_dir)
frequency = song_wav.getframerate()

# ding_wav = wave.open(ding_dir)

pygame.mixer.pre_init(frequency=frequency,
                      size=-16,
                      buffer=128,
                      channels=6,
                     )

pygame.mixer.init()       # Initialise mixer
pygame.init()             # Initialise pygame
pygame.display.set_mode() # Initialise display window   

print(pygame.mixer.get_num_channels())

# Load sounds
song = pygame.mixer.Sound(song_dir)
ding = pygame.mixer.Sound(ding_dir)

# pygame.mixer.Channel(0).play(song) # Play song on code run

while True: # Infinite loop
    for event in pygame.event.get():  # For any event (i.e. key press)
        if event.type == pygame.QUIT: # if event is a quit event, (i.e. alt-F4)
            pygame.quit()             # quit game
        if event.type == pygame.KEYDOWN:           # If a key is pressed
            if event.key == pygame.K_d:            # and the key is d,
                pygame.mixer.Channel(1).play(ding) # then play ding sound
        pygame.display.update()                    # and update display
