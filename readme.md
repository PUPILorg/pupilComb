# pupil backend

this is the backend for pupil a lecture recording service. It uses the django framework and celery to communicate between the main server and the recorders in each of the rooms

### setting up the project

1. clone the project
2. set up a conda environment with python 3.10 and install all the requirements from requirements.txt

## development guidelines

1. all models should be defined in their own file in a /models/ folder
2. each parent test folder should have a TestCaseWithData class which sets up instances of all the models in the relevant app
3. each parent test folder should have data_factory.py which defines factories for all models in the app
4. if a new model is defined make sure to import it in the `__init__.py` file in the /models/ folder and then set up a new factory in the data_factory. Then also add the factory to the relevant TestCaseWithData

## how the project is structured

1. /apps/base
   * all the base functionality for setting up schedules and recordings as well as the actual recording and storing of video
   * /models/ has all the modes
   * /tests/ houses all the tests
   * /signals/ houses all signals
   * /utils/ houses all necessary utility functions

### tests

for setting up test data [factory_boy](https://factoryboy.readthedocs.io/en/stable/index.html) is used.

1. apps/base/tests(server_tests | recorder_tests)
    * *server_tests* are tests that can be run on the server -> write all tests that don't need specific hardware access
    * *recorder_tests* tests that have to be run on the recorder -> write all tests that need hardware access here


