import pygame
import random
import time

import os
os.environ['SDL_AUDIODRIVER'] = 'alsa'

# Initialise pygame
pygame.init() 
screen = pygame.display.set_mode((600, 400))

# initialize pygame.mixer
pygame.mixer.init(frequency = 44100, size = -16, channels = 6, buffer = 20) 
# init() channels refers to mono vs stereo, not playback Channel object

background = pygame.mixer.Sound('/home/pi/Documents/pygame-stuff/4 Channel Fight/AUDIO_16_FIGHT_BASE.wav')
punch = pygame.mixer.Sound('/home/pi/Documents/pygame-stuff/4 Channel Fight/AUDIO_19_HIT_ME_2.wav')

# create separate Channel objects for simultaneous playback
channel1 = pygame.mixer.Channel(0) # argument must be int
channel2 = pygame.mixer.Channel(1)

# plays loop of rain sound indefinitely until stopping playback on Channel,
# interruption by another Sound on same Channel, or quitting pygame
channel1.play(background, loops = -1)

# plays occasional thunder sounds
duration = punch.get_length() # duration of thunder in seconds
while True: # infinite while-loop
    # play thunder sound if random condition met
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:   # If a key is pressed
            if event.key == pygame.K_SPACE:
                channel2.play(punch, loops = 0)  