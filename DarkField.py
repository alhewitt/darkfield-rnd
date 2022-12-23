import pygame
import glob
import os
import vlc

def get_sound_name_from_address(address):
    """
    :param address: address to audio file
    """
    return address.split('/')[1].rstrip('.wav')

def get_sound_files_from_folder(folder):
    """
    :param folder: address of folder containing audio files
    """
    addresses = glob.glob(folder+"*.wav")
    file_dict = {}
    for address in addresses:
        file_dict[get_sound_name_from_address(address)] = address
    return file_dict

def play_sound(sound):
    print("Loading", sound)
    instance = vlc.Instance()              # Create new instance
    media = instance.media_new(sound) # Load media file to instance
    player = vlc.MediaPlayer()            # Create players
    player.set_media(media)
    player.play()

def stop_sound(sound):
    instance = vlc.Instance()              # Create new instance
    media = instance.media_new(sound) # Load media file to instance
    player = vlc.MediaPlayer()            # Create players
    player.vlm_del_media(media)

def mins_to_ticks(time):
    m, s = time.split(':')
    return int(1000 * (int(m) * 60 + float(s)))

pygame.init()             # Initialise pygame  
pygame.display.set_mode((600, 400)) # Initialise display window   

# Load sounds
sound_files = get_sound_files_from_folder(folder = '4 Channel Bounces/')
start_time = pygame.time.get_ticks()

# Set length of button events
BUTTON_WAIT = 1.5

# Define user events
Q1_event = pygame.USEREVENT
# No audio response for Q2 so no event
Q3_event = pygame.USEREVENT + 1
leg_event = pygame.USEREVENT + 2
Q4_event = pygame.USEREVENT + 3
Q5_event = pygame.USEREVENT + 4
death_event = pygame.USEREVENT + 5

# Set timers for user events
pygame.time.set_timer(Q1_event, mins_to_ticks('0:14.5'))
pygame.time.set_timer(Q3_event, mins_to_ticks('0:44.5'))
pygame.time.set_timer(leg_event, mins_to_ticks('1:33'))
pygame.time.set_timer(Q4_event, mins_to_ticks('2:18'))
pygame.time.set_timer(Q5_event, mins_to_ticks('2:53.5'))
pygame.time.set_timer(death_event, mins_to_ticks('3:31.5'))

play_sound(sound_files['AUDIO_1'])

def time_is_between(start, end):
    start_ticks = mins_to_ticks(start)
    end_ticks = mins_to_ticks(end)
    return (pygame.time.get_ticks() - start_time) >= start_ticks and (pygame.time.get_ticks() - start_time) <= end_ticks

def button_event(time):
    start = time
    m, s = time.split(':')
    end = f'{int(m)}:{float(s)+BUTTON_WAIT}'
    if time_is_between(time, end):
        return True

Q1 = Q2 = Q3 = Q4 = Q5 = False

while True: # Infinite loop
    for event in pygame.event.get():  # For any event (i.e. key press)
        if event.type == pygame.QUIT: # if event is a quit event, (i.e. alt-F4)
            pygame.quit()             # quit game
        if event.type == pygame.KEYDOWN:           # If a key is pressed
            if event.key == pygame.K_SPACE:            # and the key is d
                if button_event('0:13'):
                    Q1 = True
                if button_event('0:16'):
                    Q2 = True
                if button_event('0:43'):
                    Q3 = True
                if button_event('2:16.5'):
                    Q4 = True
                if button_event('2:52.5'):
                    Q5 = True
                print('Key pressed')
        pygame.display.update()                    # and update display
        if event.type == Q1_event:
            print('Q1 response:', Q1)
            if Q1:
                play_sound(sound_files['AUDIO_2'])
            if not Q1:
                play_sound(sound_files['AUDIO_3'])
            pygame.time.set_timer(Q1_event, 0) 
        if event.type == Q3_event:
            print('Q3 response:', Q3)
            if Q3:
                play_sound(sound_files['AUDIO_4'])
            if not Q3:
                play_sound(sound_files['AUDIO_5'])
            pygame.time.set_timer(Q3_event, 0)
        if event.type == leg_event:
            if Q2:
                if Q1: 
                    play_sound(sound_files['AUDIO_6'])
                if not Q1:
                    play_sound(sound_files['AUDIO_7'])
            if not Q2:
                play_sound(sound_files['AUDIO_8'])
            pygame.time.set_timer(leg_event, 0)
        if event.type == Q4_event:
            print('Q4 response:', Q4)
            if Q4:
                play_sound(sound_files['AUDIO_9'])
            if not Q4:
                play_sound(sound_files['AUDIO_10'])
            pygame.time.set_timer(Q4_event, 0)
        if event.type == Q5_event:
            print('Q5 response:', Q5)
            if not Q4:
                if Q5:
                    play_sound(sound_files['AUDIO_11'])
                if not Q5:
                    play_sound(sound_files['AUDIO_12'])
            pygame.time.set_timer(Q5_event, 0)
        if event.type == death_event:
            if Q2:
                if Q1:
                    play_sound(sound_files['AUDIO_13'])
                if not Q1:
                    play_sound(sound_files['AUDIO_14'])
            if not Q2:
                play_sound(sound_files['AUDIO_15'])
            pygame.time.set_timer(death_event, 0)