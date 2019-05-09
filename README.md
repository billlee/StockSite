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

1. Navigate to "StockSite" directory
2. Call "export FLASK_APP=source"
3. Call "flask init-db"
4. Call "flask run" to start the application
5. In your browser, navigate to "localhost:5000/StockApp/" to access the home page

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
