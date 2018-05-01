import cozmo
from cozmo.util import degrees
import datetime
import time
import sys
import os
imageNumber = 0
directory = '.'
sleep_time = 10 

def on_new_camera_image(evt, **kwargs):
	now =  datetime.datetime.now()
	pilImage = kwargs['image'].raw_image
	global directory
	print("pictures/" + directory + "/" + directory + f'-{str(now)}.jpg')
	pilImage.save("pictures/" + directory + "/" + directory + f'-{str(now).replace(":", "-")}.jpg', "JPEG")
def cozmo_program(robot: cozmo.robot.Robot):
	robot.set_head_angle(degrees(5)).wait_for_completed()
	robot.set_lift_height(0.0).wait_for_completed()
	global directory
	global sleep_time
	directory = sys.argv[1]
	if len(sys.argv) > 1:
		sleep_time = int(sys.argv[2])
	if not os.path.exists('pictures'):
		os.makedirs('pictures')
	if not os.path.exists('pictures/' + directory):
		os.makedirs('pictures/' + directory)
	time.sleep(2)
	robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)
	time.sleep(sleep_time)
	print("Done: Taking Pictures")
cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
