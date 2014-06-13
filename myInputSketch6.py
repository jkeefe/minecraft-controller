#
# This script is an experiment to trigger the LEDs with a button,
# but make the middle LED fade in and out
# I learned how to do this from Make magazine, here:
# http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
#
# On the pi, you must run this script as sudo to access pins
#
# John Keefe - john@johnkeefe.net - johnnkeefe.net
# June 2014
#

import RPi.GPIO as GPIO
import time

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# pin 22, set as input. This is attached to one side of switch, ground is attached to the other.
# so we engage pull-up resistor (pull-down if to 3.3v instead of ground)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# set pin 23-25 to output for the LEDs
# LEDs are wired with pin wire to positive side (power) and ground + 330ohm resistor to negative side (ground)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

# define a pulse-wave-monitor on pin 24 for the yellow flasher
p = GPIO.PWM(24, 50)  # channel=24 frequency=50Hz
p.start(0)

toggle_state = False

# define a function to toggle the LEDs
def ledToggle():

    # to set output to high:
    # GPIO.output(12, GPIO.HIGH) or
    # GPIO.output(12, 1) or
    # GPIO.output(12, True)

    # to toggle LEDs, get the input and set it as the opposite with 'not'
    GPIO.output(23, not GPIO.input(23))
    # GPIO.output(24, not GPIO.input(24))
    GPIO.output(25, not GPIO.input(25))
    

# run an infinite loop to check the button press
while True:
    GPIO.wait_for_edge(22, GPIO.FALLING)
    print("Button 2 Pressed")
    ledToggle()
    for i in range(0,5):
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)

    GPIO.wait_for_edge(22, GPIO.RISING)
    print("Button 2 Released")
    ledToggle()



p.stop()
GPIO.cleanup()



