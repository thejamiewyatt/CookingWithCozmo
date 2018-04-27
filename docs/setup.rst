Setup
=====

1. Follow the instructions on https://www.python.org/downloads/ to download and install python 3.6.

2. Clone the repository onto your local machine.

  * ``git clone https://github.com/Msherman4231/CozmoTasteProject.git``

3. Navigate to the repository.

  * ``cd CozmoTasteProject``

4. Create a python3.6 virtual environment.

  * See `the official python tutorial <https://docs.python.org/3/tutorial/venv.html>`_ for more information.
  * It should be as easy as running the command:
    ``python3.6 -m virtualenv venv``

5. Activate your virtual environment

  *  ``source venv/bin/activate``

6. Install dependencies.

  * ``pip install -r requirements.txt``

7. With Cozmo connected, run the main program. For details on connecting Cozmo, see `Getting Started With the Cozmo SDK <http://cozmosdk.anki.com/docs/getstarted.html>`_.

  * ``python3.6 main.py``