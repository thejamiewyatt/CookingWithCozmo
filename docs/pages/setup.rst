Setup
=====

1. Follow the instructions on https://www.python.org/downloads/ to download and install python 3.6.

2. Clone the repository onto your local machine.

.. code-block:: bash

   git clone https://github.com/Msherman4231/CozmoTasteProject.git

3. Navigate to the repository.

.. code-block:: bash

   cd CozmoTasteProject

4. Create a python3.6 virtual environment. See `the official python tutorial
   <https://docs.python.org/3/tutorial/venv.html>`_ for more information.

.. code-block:: bash

   python3.6 -m virtualenv venv

5. Activate the virtual environment.

.. code-block:: bash

   source venv/bin/activate

6. Install dependencies.

.. code-block:: bash

   pip install -r requirements.txt

7. If you have an android device, follow the steps `here <http://cozmosdk.anki.com/docs/adb.html>`_ to download and install the Android Debug Bridge.

8. Follow step 1-4 under Starting Up the SDK `here <http://cozmosdk.anki.com/docs/getstarted.html#starting-up-the-sdk>`_ to connect Cozmo in SDK mode.

9. With Cozmo connected, run the main program.

.. code-block:: bash

   python3.6 main.py

10. Or skip steps 7-9 and use the -g flag to run a simulation of the program without Cozmo.

.. code-block:: bash

   python3.6 main.py -g