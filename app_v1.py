#
# Minecraft Server Controller
#
# John Keefe - john@johnkeefe.net - johnnkeefe.net
# June 2014
#
# v1 -  checks the status of a given EC2 instance and simply prints 
#       out the colored light I hope to trigger later based on the status
#
#

# import boto
import boto.ec2
import time

minecraft_instance = 'i-dbb74ff8'
connection = boto.ec2.connect_to_region('us-east-1')

def greenlight():
	print 'green light'
	
def redlight():
	print 'red light'
	
def yellowlight():
	print 'yellow light'

def start_instance(instance_id):
	# start my instance
	connection.start_instances(instance_id)

# Establish connection object
# Note: Access keys are in the config file ~/.boto


# One infinite loop
x = 1
while x == 1:
	
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
		
	# wait x seocons
	time.sleep(3)
	
	


		