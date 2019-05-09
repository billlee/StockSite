# StockSite
Software Engineering Web Applications Project


## Server-side Instructions 
Follow these steps to run:

1. Install virtualenv to create a virtual environment
```console
foo@bar:~$ pip3 install virtualenv
```

2. Create and start a virtual environment to install the necessary packages
```console
foo@bar:~$ virtualenv venv
foo@bar:~$ source venv/bin/activate
```

3. Install the necessary python packages
```console
foo@bar:~$ pip3 install -r requirements.txt
```

4. Navigate to "StockSite" directory
5. Call "export FLASK_APP=source"
6. Call "flask init-db"
7. Call "flask run" to start the application
8. In your browser, navigate to "localhost:5000/StockApp/" to access the home page

```console
foo@bar:~$ cd StockSite
foo@bar:~$ export FLASK_APP=source
foo@bar:~$ flask init-db
Initialized the database.
foo@bar:~$ flask run
 * Serving Flask app "source"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## File Locations
StockSite/csv contains the dump of our database
StockSite/diagrams contains our UML and system diagram
StockSite/source contains all of our code:

source/database contains our database and SQL entry points
source/neuralNet contains the program to run the NeuralNet predictor
source/static contains the images rendered by our HTML, as well as the style.css file
source/templates contains all of the HTML displayed in the UI

Other Files:
__init__.py is the main entrypoint for Flask
main.py is the bulk of our Python code, handles all requests between API, UI, database, and predictors
bayesian_curve_fitting.py is the program that run the Bayesian predictor