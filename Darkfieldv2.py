import pygame
import glob
import vlc
import wiringpi    
    
'''
Issues:

- If you answered no to Q3, there is a slight overlap with the sounds while you fall asleep
- If you don't go back to the room, the death scene happens too early

Ideas:

- Try allowing two long sounds at once again
- Use something other than pygame for timing (might be more accurate)
'''

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
    
def merge_dicts(dict1, dict2):
    return(dict2.update(dict1))

# Initialise pygame
pygame.init() 
screen = pygame.display.set_mode((600, 400))

# initialise wiringpi
wiringpi.wiringPiSetup()

# define GPIO mode
GPIO23 = 4
GPIO24 = 5
GPIO25 = 6
GPIO26 = 25
LOW = 0
HIGH = 1
OUTPUT = 1
INPUT = 0
PULL_DOWN = 1
wiringpi.pinMode(GPIO23, OUTPUT) # button LED
wiringpi.pinMode(GPIO25, OUTPUT) # water splash LED
wiringpi.pinMode(GPIO26, OUTPUT) # fan
wiringpi.pinMode(GPIO24, INPUT)  # push button
wiringpi.pullUpDnControl(GPIO24, PULL_DOWN) # pull down

# Define colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define lengths of time
BUTTON_WAIT = '0:01.5'

# Define number of previous short sounds loaded at once
SHORT_SOUNDS_LOADED = 0

# Define events
button_on_event = pygame.USEREVENT
button_off_event = pygame.USEREVENT + 1
sound_event = pygame.USEREVENT + 2
next_event = pygame.USEREVENT + 3
end_fight = pygame.USEREVENT + 4

# Load sounds
sound_files = get_sound_files_from_folder(folder = '4 Channel Bounces/')
merge_dicts(get_sound_files_from_folder(folder = '4 Channel Fight/'), sound_files)

# Define start_time
start_time = pygame.time.get_ticks()

# Define players list with players[0] being short sounds and players[1] being long
players = [[],[]]
short_players = players[0]
long_players = players[1]


# Stores answers to each question with a buffer for Q[0] so the numbers match
Q = [0, False, False, False, False, False]

def play_sound(sound):
    while len(short_players) > SHORT_SOUNDS_LOADED:
        stop_sound(short_players[0])
        short_players.pop(0)
    print("Loading", sound)
    instance = vlc.Instance()         # Create new instance
    media = instance.media_new(sound) # Load media file to instance
    player = vlc.MediaPlayer()        # Create players
    player.set_media(media)
    player.play()
    return player

def stop_sound(player):
    player.release()

def mins_to_ticks(time):
    m, s = time.split(':')
    return int(1000 * (int(m) * 60 + float(s)))

# Turn off all GPIO outputs being used
def turn_all_off():
    wiringpi.digitalWrite(GPIO23, LOW) # Button light
    wiringpi.digitalWrite(GPIO25, LOW) # LED
    wiringpi.digitalWrite(GPIO26, LOW) # Fan

def turn_on_button():
    print('Button on')
    wiringpi.digitalWrite(GPIO23, HIGH)  

def turn_off_button():
    print('Button off')
    wiringpi.digitalWrite(GPIO23, LOW)

def wait_until(time):
    time = mins_to_ticks(time)
    now = pygame.time.get_ticks()
    wait = time-(now-start_time)
    return wait

def get_press():
    return wiringpi.digitalRead(GPIO24)

def get_button_response_in_window(window=BUTTON_WAIT, Q=False, button_off=True):
    turn_on_button()
    if type(window) == str: window = mins_to_ticks(window)
    button_start_time = pygame.time.get_ticks()
    print('timer started')
    if button_off: pygame.time.set_timer(button_off_event, window, loops=1)
    pressed = 0
    while (pygame.time.get_ticks() - button_start_time) < window and pressed == 0:
        if get_press():
            Q = True
            pressed = 1
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     Q = True
    return Q

#=======================================================================================#
# This function contains all events
def perform_event(event_number, Q):
    # Q1 = Q[1] etc
    
    # Q1 at '0:13'
    if event_number == 1:
        pygame.time.set_timer(next_event, mins_to_ticks(BUTTON_WAIT), loops=1)
        Q[1] = get_button_response_in_window(button_off=False)

    # Q1 response at '0:14.5'
    elif event_number == 2:
        pygame.time.set_timer(next_event, mins_to_ticks('0:01.5'), loops=1)
        turn_off_button()
        if Q[1]: short_players.append(play_sound(sound_files['AUDIO_2']))
        else: short_players.append(play_sound(sound_files['AUDIO_3']))

    # Q2 at '0:16'
    elif event_number == 3:
        Q[2] = get_button_response_in_window()
        pygame.time.set_timer(next_event, wait_until('0:43'), loops=1)

    # Q3 at '0:43'
    elif event_number == 4:
        Q[3] = get_button_response_in_window(button_off=False)
        pygame.time.set_timer(next_event, mins_to_ticks(BUTTON_WAIT), loops=1)

    # Q3 response at '0:44.5'
    elif event_number == 5:
        turn_off_button()
        if Q[3]: short_players.append(play_sound(sound_files['AUDIO_4']))
        else: short_players.append(play_sound(sound_files['AUDIO_5']))
        pygame.time.set_timer(next_event, wait_until('1:33'), loops=1)

    # Kick out legs at '1:33'
    elif event_number == 6:
        if not Q[2]: short_players.append(play_sound(sound_files['AUDIO_8']))
        elif Q[1] and Q[2]: short_players.append(play_sound(sound_files['AUDIO_6']))
        else: players.append(play_sound(sound_files['AUDIO_7']))
        pygame.time.set_timer(next_event, wait_until('2:16.5'), loops=1)

    # Q4 at '2:16.5'
    elif event_number == 7:
        Q[4] = get_button_response_in_window(button_off=False)
        pygame.time.set_timer(next_event, mins_to_ticks(BUTTON_WAIT), loops=1)

    # Q4 response at '2:18'
    elif event_number == 8:
        turn_off_button()
        stop_sound(long_players[0]) # stop AUDIO_1
        long_players.pop(0) # Remove stopped audio from list
        if Q[4]:
            long_players.append(play_sound(sound_files['AUDIO_9']))
            event_number = 10 # In order to skip events 9 and 10
            pygame.time.set_timer(next_event, wait_until('3:28.5'), loops=1)
        else:
            long_players.append(play_sound(sound_files['AUDIO_10']))
            pygame.time.set_timer(next_event, wait_until('2:52.5'), loops=1)

    # Q5 at '2:52.5'
    elif event_number == 9:
        if not Q[4]:
            Q[5] = get_button_response_in_window(window='0:01', button_off=False)
            pygame.time.set_timer(next_event, mins_to_ticks('0:01'), loops=1)
    
    # Q5 response at '2:53.5'
    elif event_number == 10:
        turn_off_button()
        if not Q[4]:
            stop_sound(long_players[0]) # Stop AUDIO_10
            long_players.pop(0) # Remove stopped audio from list
            if Q[5]: long_players.append(play_sound(sound_files['AUDIO_11']))
            else: long_players.append(play_sound(sound_files['AUDIO_12']))
        pygame.time.set_timer(next_event, wait_until('3:28.5'), loops=1)
        
    # Death scene at '3:28.5'
    elif event_number == 11:
        stop_sound(long_players[0])
        long_players.pop(0)
        if not Q[2]: long_players.append(play_sound(sound_files['AUDIO_15']))
        elif Q[1] and Q[2]: long_players.append(play_sound(sound_files['AUDIO_13']))
        else: long_players.append(play_sound(sound_files['AUDIO_14']))

    return Q, event_number
        
#=======================================================================================#

# First event: Play audio 1
long_players.append(play_sound(sound_files['AUDIO_1']))
event_number = 1
pygame.time.set_timer(next_event, mins_to_ticks('0:13'), loops=1)

while True:
    for event in pygame.event.get():  # For any event (i.e. key press)
        if event.type == pygame.QUIT: # if event is a quit event, (i.e. alt-F4)
            pygame.quit()             # quit game
        if event.type == next_event:
            print('Event:', event_number)
            Q, event_number = perform_event(event_number, Q)
            event_number += 1
        if event.type == button_off_event:
            turn_off_button()
