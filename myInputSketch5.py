import RPi.GPIO as GPIO

#set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# pin 22, set as input. This is attached to one side of switch, ground is attached to the other.
# so we engage pull-up resistor (pull-down if to 3.3v instead of ground)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# set pin 23-25 to output for the LEDs
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

def ledToggle(channel):

	# to set output to high:
	# GPIO.output(12, GPIO.HIGH) or
	# GPIO.output(12, 1) or
	# GPIO.output(12, True)

	# to toggle LEDs, get the input and set it as the opposite with 'not'
	GPIO.output(23, not GPIO.input(23))
	GPIO.output(24, not GPIO.input(24))
	GPIO.output(25, not GPIO.input(25))

# GPIO.add_event_detect(22, GPIO.RISING, callback=ledToggle, bouncetime=300)

while True:
	GPIO.wait_for_edge(22, GPIO.FALLING)
	print("Button 2 Pressed")
	ledToggle()

	GPIO.wait_for_edge(22, GPIO.RISING)
	print("Button 2 Released")
	ledToggle()

GPIO.cleanup()

# must run this script as sudo to access pins

