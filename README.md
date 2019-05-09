# StockSite
Software Engineering Web Applications Project


## Server-side Instructions 
Follow these steps to run:

1. Install Flask on your system
    * In Linux, run "pip install flask"
    * In Windows, locate installation online
    * On Mac OS X, run the following command (if both Python 2 and Python 3 are installed)
    
```console
foo@bar:~$ pip3 install flask
```
1. Navigate to "StockSite" directory
2. Call "export FLASK_APP=source"
3. Call "flask init-db"
4. Call "flask init-companies"
5. Call "flask init-historical"
6. Call "flask run" to start the application
7. In your browser, navigate to "localhost:5000/StockApp/" to access the home page

```console
foo@bar:~$ export FLASK_APP=source
foo@bar:~$ flask init-db
Initialized the database.
foo@bar:~$ flask init-companies
Initialized the database.
foo@bar:~$ flask init-historical
Initialized the database.
foo@bar:~$ flask run
 * Serving Flask app "source"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
