import pygame
from pygame.locals import *
import os

# Set working directory
os.chdir('C:/Users/amyhe/OneDrive/Documents/GitHub/pygame-stuff/')

pygame.init()             # Initialise pygame  
pygame.mixer.init()       # Initialise mixer
pygame.display.set_mode() # Initialise display window   

# Import sounds
song1 = pygame.mixer.Sound('sounds/song.wav')
song2 = pygame.mixer.Sound('sounds/song2.wav')
ding = pygame.mixer.Sound('sounds/ding.wav')

pygame.mixer.Channel(0).play(song1) # Play song on code run

while True: # Infinite loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # Enable quitting
            pygame.quit(); 
        if event.type == pygame.KEYDOWN:           # If a key is pressed
            if event.key == pygame.K_m:            # and the key is m,
                pygame.mixer.Channel(1).play(ding) # then play ding sound
        pygame.display.update()                    # and update display
