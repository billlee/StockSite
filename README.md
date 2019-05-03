# StockSite
Software Engineering Web Applications Project

Follow these steps to run:

1. Install Flask on your system
    a. In Linux, run "pip install flask"
    b. In Windows, locate installation online
1. Navigate to "StockSite" directory
2. Call "export FLASK_APP=flaskr"
3. Call "flask init-db"
4. Call "flask init-companies"
5. Call "flask init-historical"
6. Call "flask run" to start the application
7. In your browser, navigate to "localhost:5000/StockApp/" to access the home page

```console
foo@bar:~$ export FLASK_APP=flaskr
foo@bar:~$ flask init-db
Initialized the database.
foo@bar:~$ flask init-companies
Initialized the database.
foo@bar:~$ flask init-historical
Initialized the database.
foo@bar:~$ flask run
 * Serving Flask app "flaskr"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
