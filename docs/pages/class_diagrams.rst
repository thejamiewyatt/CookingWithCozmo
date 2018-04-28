Class Diagrams
==============
We have leveraged object oriented programming significantly in this project. Please review the following
inheritance diagrams. Notice that in 3 different packages we have one abstract base class and multiple
inheriting classes.


Robot Package
-------------
.. inheritance-diagram::
   cozmo_taste_game.robot.cozmo_robot
   cozmo_taste_game.robot.fake_robot
   :parts: 1

The robot package has a Fake Robot and Cozmo Robot that both inherit from a abstract robot base class.
Methods that are publicly called from main() must be included in the abstract base class and implemented
in both of the inheriting classes. This allows the program to be ran without Cozmo which allows
developers that do not have access to Cozmo to develop program control flow.

Plate Package
-------------
.. inheritance-diagram::
   cozmo_taste_game.plate.colorful_plate
   :parts: 1

The plate package contains different plates. A different Plate can easily be instantiated in main() which
allows for a different twist on the game. Many Plates could be added to this package like a dessert plate
or vegetarian plate!

Food Package
------------
.. inheritance-diagram::
   cozmo_taste_game.food.food_props
   :parts: 1

The food package includes all the different Food classes that inherit from the abstract Food Prop class.
Each food class has properties that vary like colors.


