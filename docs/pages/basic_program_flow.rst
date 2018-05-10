Basic Program Flow
===================

The program has 3 parts: image capture, the game loop, and the food analyzer.

Image Capture
------------------

When the program first starts, it ties cozmo's camera event
to the on_new_camera_image() function, which is then called asynchronously by the Cozmo api.
Every time cozmo has a new image in its buffer. The program then saves the image to disk
and stores its location in the global variable 'photo_location'. Another image will not be taken until the game loop has
consumed the image and sets 'photo_location' to None.

Game Loop
------------

The game loop is very simple. The game loop checks to see if 'photo_location' isn't None. If it is, the program
forwards 'photo_location' to the food analyzer, which is where all of the tensorflow image recognition is done.
After the program is done analyzing the photo, it checks to see if a valid food was found. If there is a valid food,
the game performs an action with the food, which in our case is trying to add it to the plate.

Food Analyzer
----------------

The food analyzer is where all the filtering is done for image recognition. Sometimes when Cozmo see's an image, there may
be a false positive. This is why inside the food analyzer, when it thinks it sees something, it will keep track of previous
foods and will only say that it has found food when it is fully confident.

One implementation could be to only be confident
when the analyze_photo function has a max confidence above .6 3 times in a row. This is conservative, but it will filter
out any potential false positives.


**References**

:mod:`cozmo_taste_game.image_recognition.response_analyzer`