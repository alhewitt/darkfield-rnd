import pygame
import glob
import vlc
import wiringpi
import time
    
'''
Issues:

- If you answered no to Q3, there is a slight overlap with the sounds while you fall asleep
- If you don't go back to the room, the death scene happens too early

Ideas:

- Try allowing two long sounds at once again
- Find limits for simultanious sounds
- Check how long it takes to load a sound in (might be worth pre-loading)
- Use something other than pygame for timing (might be more accurate)
- Have a user object with attributes such as gender, punches, certain question responses etc
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
fight_start_event = pygame.USEREVENT + 4
fight_end_event = pygame.USEREVENT + 5

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
    while len(short_players) >= 1:
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
    return Q

def play_punch_sound(punches):
    for player in short_players:
        print('stopping', player)
        stop_sound(player)
    seventh = False
    if punches == 1:
        short_players.append(play_sound(sound_files['AUDIO_23_PUNCH_2']))
    elif punches == 2:
        short_players.append(play_sound(sound_files['AUDIO_23_PUNCH_2']))
    elif punches == 3:
        short_players.append(play_sound(sound_files['AUDIO_23_PUNCH_2']))
    elif punches == 4:
        short_players.append(play_sound(sound_files['AUDIO_23_PUNCH_2']))
    elif punches == 5:
        short_players.append(play_sound(sound_files['AUDIO_23_PUNCH_2']))
    elif punches == 6:
        short_players.append(play_sound(sound_files['AUDIO_23_PUNCH_2']))
    elif punches == 7:
        pygame.time.set_timer(fight_end_event, 0)
        short_players.append(play_sound(sound_files['AUDIO_23_PUNCH_2']))
        end_fight()
        seventh = True
    return seventh        
        

def get_punches_until(end):
    punches = 0
    ended = False
    while (pygame.time.get_ticks() - start_time) < end and ended == False:
        if get_press():
            turn_off_button()
            punches += 1
            ended = play_punch_sound(punches)
            print(punches, ended)
            time.sleep(2)
            turn_on_button()
            
            
    
def begin_fight():
    turn_on_button()
    fight_start_time = pygame.time.get_ticks()
    pygame.time.set_timer(fight_end_event, mins_to_ticks('1:00'), loops=1)
    punches = 0
    print('Fight started')
    get_punches_until(wait_until('1:02'))
    
def end_fight():
    turn_off_button()
    
    
#=======================================================================================#
# This function contains all events
def perform_event(event_number, Q):
    # Fight at '3:42
    if event_number == 12:
#         stop_sound(long_players[0])
#         long_players.pop(0)
        long_players.append(play_sound(sound_files['AUDIO_16_FIGHT_BASE']))
        time.sleep(2)
        begin_fight()
        turn_off_button()
        

    return Q, event_number
        
#=======================================================================================#

# First event: Play audio 1
# long_players.append(play_sound(sound_files['AUDIO_1']))
# event_number = 1
# pygame.time.set_timer(next_event, mins_to_ticks('0:13'), loops=1)

# Uncomment this to skip straight to a certain point
event_number = 12
pygame.time.set_timer(next_event, mins_to_ticks('0:1'), loops=1)

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
        if event.type == fight_start_event:
            begin_fight()
        if event.type == fight_end_event:
            end_fight()
