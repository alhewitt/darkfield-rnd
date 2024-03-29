# ch01_02.py file
import wiringpi
# import wiringpi2 as wiringpi

# initialize
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
wiringpi.pinMode(GPIO23, OUTPUT)  # button LED
wiringpi.pinMode(GPIO25, OUTPUT) # water splash LED
wiringpi.pinMode(GPIO26, OUTPUT) # fan
wiringpi.pinMode(GPIO24, INPUT)  # push button
wiringpi.pullUpDnControl(GPIO24, PULL_DOWN)  # pull down


# make all LEDs off
def clear_all():
    wiringpi.digitalWrite(GPIO23, LOW)

try:
    clear_all()
    while 1:
        button_state = wiringpi.digitalRead(GPIO24)
        if button_state == 1:
            wiringpi.digitalWrite(GPIO23, HIGH)
            wiringpi.digitalWrite(GPIO25, HIGH)
            wiringpi.digitalWrite(GPIO26, HIGH)
        else:
            wiringpi.digitalWrite(GPIO23, LOW)
            wiringpi.digitalWrite(GPIO25, LOW)
            wiringpi.digitalWrite(GPIO26, LOW)

        wiringpi.delay(20)

except KeyboardInterrupt:
    clear_all()

print("done")