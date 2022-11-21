import pygame
from pygame.locals import *
import os
import time

os.chdir('C:/Users/amyhe/OneDrive/Documents/Visual Studio 2019/')

pygame.init()
width = 1000
height = 500
window = pygame.display.set_mode((width,height))
pygame.mixer.init()
pygame.display.set_mode() 

song1 = pygame.mixer.Sound('sounds/song.wav')
song2 = pygame.mixer.Sound('sounds/song2.wav')
ding = pygame.mixer.Sound('sounds/ding.wav')


# while True:
#     pygame.mixer.Channel(0).play(song1)
#     # pygame.mixer.Channel(1).play(song2)
#     # time.sleep(5)
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             break
#         if event.type == KEYDOWN:
#             pygame.mixer.Channel(1).play(song2)
#             time.sleep(5)

# ding = pygame.mixer.Sound(dingfile)

pygame.mixer.Channel(0).play(song1)

while True:
    # time.sleep(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pygame.mixer.Channel(1).play(ding)
        pygame.display.update()




# pygame.mixer.Channel(2).play(ding)
