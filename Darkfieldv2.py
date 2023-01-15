import pygame
import glob
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
    return player

def stop_sound(player):
    player.release()

def mins_to_ticks(time):
    m, s = time.split(':')
    return int(1000 * (int(m) * 60 + float(s)))

def merge_dicts(dict1, dict2):
    return(dict2.update(dict1))
    
# Initialise pygame
pygame.init() 
screen = pygame.display.set_mode((600, 400))

# Define colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define lengths of time
BUTTON_WAIT = '0:01.5'

# Define number of short sounds loaded at once
SOUNDS_LOADED = 1

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

# Define players list
players = []

# First event: Play audio 1
player0 = play_sound(sound_files['AUDIO_1'])
event_number = 1
pygame.time.set_timer(next_event, mins_to_ticks('0:13'), loops=1)

def turn_on_button():
    print('Button on')
#    screen.fill(RED)
#    pygame.display.flip()
#    pygame.display.update()  

def turn_off_button():
    print('Button off')
#    screen.fill(BLACK)
#    pygame.display.flip()
#    pygame.display.update() 

def wait_until(time):
    time = mins_to_ticks(time)
    now = pygame.time.get_ticks()
    wait = time-(now-start_time)
    return wait

def get_button_response_in_window(window=BUTTON_WAIT, Q=False, button_off=True):
    turn_on_button()
    if type(window) == str: window = mins_to_ticks(window)
    button_start_time = pygame.time.get_ticks()
    print('timer started')
    if button_off: pygame.time.set_timer(button_off_event, window, loops=1)
    while (pygame.time.get_ticks() - button_start_time) < window:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Q = True
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
        if Q[1]: players.append(play_sound(sound_files['AUDIO_2']))
        else: players.append(play_sound(sound_files['AUDIO_3']))

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
        if Q[3]: players.append(play_sound(sound_files['AUDIO_4']))
        else: players.append(play_sound(sound_files['AUDIO_5']))
        pygame.time.set_timer(next_event, wait_until('1:33'), loops=1)

    # Kick out legs at '1:33'
    elif event_number == 6:
        if not Q[2]: players.append(play_sound(sound_files['AUDIO_8']))
        elif Q[1] and Q[2]: players.append(play_sound(sound_files['AUDIO_6']))
        else: players.append(play_sound(sound_files['AUDIO_7']))
        pygame.time.set_timer(next_event, wait_until('2:16.5'), loops=1)

    # Q4 at '2:16.5'
    elif event_number == 7:
        Q[4] = get_button_response_in_window(button_off=False)
        pygame.time.set_timer(next_event, mins_to_ticks(BUTTON_WAIT), loops=1)

    # Q4 response at '2:18'
    elif event_number == 8:
        turn_off_button()
        stop_sound(player0)
        if Q[4]: player4 = play_sound(sound_files['AUDIO_9'])
        else: player4 = play_sound(sound_files['AUDIO_10'])
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
            stop_sound(player4)
            if Q[5]: player5 = append(play_sound(sound_files['AUDIO_11']))
            else: player5 = append(play_sound(sound_files['AUDIO_12']))
        pygame.time.set_timer(next_event, wait_until('3:28.5'), loops=1)

    elif event_number == 11:
        if Q[4]: stop_sound(player4)
        else: stop_sound(player5)
        
        if not Q[2]: players.append(play_sound(sound_files['AUDIO_15']))
        elif Q[1] and Q[2]: players.append(play_sound(sound_files['AUDIO_13']))
        else: players.append(play_sound(sound_files['AUDIO_14']))

    return Q
        
#=======================================================================================#

# Stores answers to each question with a buffer for Q[0] so the numbers match
Q = [0, False, False, False, False, False]

while True:
    for event in pygame.event.get():  # For any event (i.e. key press)
        if event.type == pygame.QUIT: # if event is a quit event, (i.e. alt-F4)
            pygame.quit()             # quit game
        if event.type == next_event:
            while len(players) > SOUNDS_LOADED:
                stop_sound(players[0])
                players.pop(0)
            Q = perform_event(event_number, Q)
            event_number += 1
        if event.type == button_off_event:
            turn_off_button()
