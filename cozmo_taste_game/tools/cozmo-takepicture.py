import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import time
import sys
import os

# GLOBALS
imageNumber = 0
directory = '.'
takePicture = True
def on_new_camera_image(evt, **kwargs):
    global takePicture
    if takePicture:
        pilImage = kwargs['image'].raw_image
        pilImage.save(f"test.jpg", "JPEG")
        takePicture = False




def cozmo_program(robot: cozmo.robot.Robot):
    global takePicture
    # Make sure Cozmo's head and arm are at reasonable levels
    robot.set_head_angle(degrees(1)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()

  
    # Anytime Cozmo sees a "new" image, take a photo
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)
  
    # And we're done here
    #robot.say_text("All done!").wait_for_completed()
    #robot.camera.enable_auto_exposure(False)
    #robot.camera.set_manual_exposure( 5, .5)
    
    while takePicture == True:
        pass
    #robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()
    

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
