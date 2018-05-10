How to Train Cozmo to Recognize a New Food
==========================================

**All the python scripts used in this section are located in the cozmo_taste_game/tools folder**

It's best to have some general knowlege about neural networks and tensorflow when retraining cozmo. Here are some
resources that may be helpful to read before continuing:

	- `General information about retraining <https://www.tensorflow.org/tutorials/image_retraining/>`_
	- `Information about retrain.py and its arguments <https://hackernoon.com/creating-insanely-fast-image-classifiers-with-mobilenet-in-tensorflow-f030ce0a2991/>`_
	- `More information about retraining <https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/>`_

It should also be noted that you should have similar training and real world operating. Ex: if you're training Cozmo
and there's a white background, there should be a white background when the program is running. White is a really
good color choice since it provides good contrast between the background and the images.

Cozmo uses a retrained MobileNet neural network to classify images. Training the network has
3 steps:

1. Take images with Cozmo:
---------------------------------

    To take pictures with cozmo, place him and his testing plate on their respective locations on the mat.
    Execute "take-pictures.py <food_name> <duration>" where duration is how long cozmo will take pictures.
    This command will save .jpg images to pictures/<food_name>/. Once you execute the script rotate the food on
    the plate or rotate cozmo, making sure cozmo sees all the sides he would see during the game. 
	
	How you do it doesn't matter, as long as
	the pictures are clear and cozmo is the correct distance from the food (about the distance between him and the plate during gameplay).
	800 to 1,000 pictures is a good amount of pictures, just be sure that all objects have about the same number of pictures.
  
    After you finish taking the pictures, review them. While reviewing them, remove any pictures that aren't good quality.
    Some examples are:
		1. Images that have an foreign object in frame (Ex: your hand)
		2. Images that are blurry

    The picture taking process takes a lot of experimentation. If the neural network isn't training well, you can try
    taking pictures with brighter/darker lighting, adding more pictures, or removing pictures that are poor quality.

  
2. Run the training script:
---------------------------------

    For this next step, you will be running a script that trains the neural network. The first step is to copy the folders
    in "pictures" to the "data" folder. Then, open a console that is in the image recognition folder
    ( Shift+Right click then click open command window here in Windows). Run the command:

	.. code-block:: bash

		python retrain.py --image_dir=./data --how_many_training_steps=1000  --validation_batch_size=-1 --train_batch_
		size=32 --validation_percentage=20 --testing_percentage=20 --learning_rate=.01 --architecture mobilenet_1.0_224

    This command will begin training the network. 
	
	 **Note:** *Typing retrain.py -\\-help  will give you some information about the arguments that are supplied*

    Once the training is complete, there will be 2 files in ./output:
        1. output_graph.pb: This is the actual model
        2. output_labels.txt: This has the names of the foods

    There will also be 3 folders. None of them are important except for retrain_logs, which contains logs that can be used with
    tensorboard (read .


3. Test (and possibly repeat all 3 steps):
--------------------------------------------------

    The final step is to test your neural network. Connect your phone to cozmo and the computer, then position
    Cozmo, the plate, and a food item on the plate. Run the program "Cozmo-takepicture.py". This program will take a picture
    and save it in the same directory as test.jpg. Then run "mobile-net-test.py" to run "test.jpg" through the network. You can also
	supply an argument to test an image with a different name. Ex: "mobile-net-test apple" will run the test on "apple.jpg".

    The program will eventually print out a dictionary with the values **{'food_name_1': prediction_confidence, ..., 'food_name_5': prediction_confidence}**
    These values are the network's predictions and confidence levels in descending order, where 'food_name_1' is the most likely classification,
    and 'food_name_5' is the least likely.

    Do this test for all the food props. I recommend taking, and then testing two or more pictures without moving cozmo. This is because Cozmo's
    camera is very visually noisy, and the noise can impact the results. Getting a bigger sample size gives a better picture of the accuracy.
    It is best to consistently get a correct guess with a confidence of .90 or greater in most positions. 

    If your network is performing correctly, then you are finished. You can now replace the model files (**output_graph.pb** and **output_labels.txt**)
    that are in the resource folder with your newly created files. It is wise to keep backups of the old models just in case your new one has
    issues in the future.

    if your network isn't performing well, read the troubleshooting tips below, and then go back to step 1.


Neural Network Troubleshooting
-----------------------------------

    Here are some tips to improve your neural networks accuracy:
	
        1. Don't use similar looking props (ex: a lemon and a lime). Since Cozmo can't see color, his
           camera isn't good, telling the difference between similar props is nearly impossible.

		   
        2. If one food prop is giving you trouble, sometimes deleting, and then retaking all of its images is better than
           just adding new images.

		   
        3. If you notice you have a high training accuracy but low validation accuracy, this usually means you don't have
           enough images or that your images don't have enough variance.
