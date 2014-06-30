#
# Minecraft Server Controller
#
# John Keefe - john@johnkeefe.net - johnnkeefe.net
# June 2014
#
# v1 -  checks the status of a given EC2 instance and simply prints 
#       out the colored light I hope to trigger later based on the status
#
# v2 -  actually trigger the red, green or yellow flashing lights based on 
#       the status of the EC2 instance
#

# import boto
import boto.ec2
import RPi.GPIO as GPIO
import time

# set these variables for the EC2 instance
minecraft_instance = 'i-dbb74ff8'
connection = boto.ec2.connect_to_region('us-east-1')


# The connection line above establishes the connection object
# Note: Access keys are in the config file ~/.boto  (for a user)
#       But on the pi, since we're running under sudo to get the pins, needs to be at /etc/boto.cfg
#       See details at http://boto.readthedocs.org/en/latest/boto_config_tut.html



#set up the raspberry pi's GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# set pin 23-25 to output for the LEDs
# LEDs are wired with pin wire to positive side (power) and ground + 330ohm resistor to negative side (ground)
GPIO.setup(23, GPIO.OUT) # Green
GPIO.setup(24, GPIO.OUT) # Yellow
GPIO.setup(25, GPIO.OUT) # Red

# define a pulse-wave-monitor on pin 24 for the yellow flasher
# so that it can fade in and out (an aesthetic touch)
p = GPIO.PWM(24, 50)  # channel=24 frequency=50Hz
p.start(0)

# pin 22, set as input. This is attached to one side of switch, ground is attached to the other.
# so we engage pull-up resistor (pull-down if to 3.3v instead of ground)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def allLightsOff():
    # turns all lights off to reset
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(25, False)

def greenlight():
    print 'green light'
    # reset all lights
    allLightsOff()
    # illuminate the green one
    GPIO.output(23, True)  

def redlight():
    print 'red light'
    # reset all lights
    allLightsOff()
    # illuminate the red one
    GPIO.output(25, True)

def yellowlight():
    print 'yellow light'
    allLightsOff()
    # cycle the flashing yellow (p) 5 times
    for i in range(0,5):
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)

def start_instance(instance_id):
    # start my instance
    connection.start_instances(instance_id)
    
def startupServer(channel):
    # This function runs when the button is pushed
    # Note the listener passes one argument, which is the pin that is triggered (channel)
    start_instance(minecraft_instance)
    starting = True
    while starting == True:
        yellowlight()
        # check to see if the server is running yet
        # if it is, set the green light and bail out of this loop
        if my_instance.state == 'running':
            greenlight()
            starting = False
        time.sleep(5)


# set up an event listner for a button press on GPIO 22
# such that a button press triggers the flashing yellow
GPIO.add_event_detect(22, GPIO.FALLING, callback=startupServer, bouncetime=300)

# One infinite loop
while True:
    
    # get fresh instance object
    # note connection.get_only_instances() returns an array of all instances
    # here just want the matching one, we limit it such that it returns a list of one
    instance_list = connection.get_only_instances(instance_ids=[minecraft_instance])
    
    # the single instance we fetched will be available as instance_list[0]
    my_instance = instance_list[0]

    if my_instance.state == 'running':
        greenlight()
    elif my_instance.state == 'stopped':
        redlight()
    elif my_instance.state == 'stopping' or my_instance.state == 'pending':
        yellowlight()
    else:
        print 'unknown status: %s' % my_instance.state
        
    # wait x seconds
    time.sleep(30)
