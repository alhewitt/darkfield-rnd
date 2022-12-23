import pygame
from pygame.locals import *
import os
import vlc

# Set working directory
os.chdir('C:/Users/amyhe/OneDrive/Documents/GitHub/pygame-stuff/')

pygame.init()             # Initialise pygame  
pygame.mixer.init()       # Initialise mixer
pygame.display.set_mode() # Initialise display window   

# Load sounds
song1 = pygame.mixer.Sound('sounds/song.wav')
song2 = pygame.mixer.Sound('sounds/song2.wav')
ding = pygame.mixer.Sound('sounds/ding.wav')

pygame.mixer.Channel(0).play(song1) # Play song on code run

while True: # Infinite loop
    for event in pygame.event.get():  # For any event (i.e. key press)
        if event.type == pygame.QUIT: # if event is a quit event, (i.e. alt-F4)
            pygame.quit()             # quit game
        if event.type == pygame.KEYDOWN:           # If a key is pressed
            if event.key == pygame.K_d:            # and the key is d,
                pygame.mixer.Channel(1).play(ding) # then play ding sound
        pygame.display.update()                    # and update display
