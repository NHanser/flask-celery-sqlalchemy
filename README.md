# Flask + Celery + SQLAlchemy Example App

This example app demonstrates how to write Celery tasks that work with Flask and
SQLAlchemy. I had a hard time finding a complete example that worked correctly.

Based on the [the Flask-User-Starter-App](https://github.com/lingthio/Flask-User-starter-app).
Other references : 

## Code characteristics

* Tested on Python 3.10
* Well organized directories with lots of comments
    * app
        * celeryapp
        * core
        * dashapp
        * oauth
        * rssapp
        * static
        * templates

        * commands.py
        * extensions.py
        * scheduled_tasks.py
        * settings.py

        
    * tests
* Includes test framework (`py.test`)
* Includes database migration framework (`alembic`)
* Sends error emails to admins for unhandled exceptions


## Setting up a development environment

We assume that you have `git` and `virtualenv` and `virtualenvwrapper` installed. For Windows, install pipenv.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/NHanser/flask-celery-sqlalchemy.git my_app

    # Create the 'my_app' virtual environment using virtualenv
    cd ~/dev/my_app
    py -3 -m venv venv # Windows command
    OR  
    mkvirtualenv -p PATH/TO/PYTHON my_app # Linux/MacOs command

    # Install required Python packages
    .\venv\Scripts\Activate.ps1 # Windows powershell
    OR
    workon my_app # Linux or MacOS

    #Then
    pipenv install


# Configuring SMTP

Copy the `.env_template` file to `.env`.

    cp .env_template .env

Edit the `.env` file.

Specifically set all the MAIL_... settings to match your SMTP settings

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en

Note that Yahoo's SMTP server requires the configuration of "Allow apps that use less secure sign in".
See https://help.yahoo.com/kb/SLN27791.html


## Initializing the Database
##### Create local postgresql database
    mkdir -p ~/dev/my_app/postgresql-data
##### Create DB tables and populate the roles and users tables
    flask db init
    flask db migrate -m "Initial version"
    flask db upgrade

##### Fill the database with 2 sample users
    flask init create-users
##### create feeds (optional)
    flask init create-feeds

## Debug the app
### Set environment
Copy template file

    cp dev/docker.env.template dev/docker.env
    
Then edit dev/docker.env

### Docker compose
    docker compose -f "dev/docker-compose.yml" up -d --build

### Launch debug configuration in VSCode
If you don't launch debugger, application will not start

    {
        "name": "Python: Remote Attach",
        "type": "python",
        "request": "attach",
        "port": 5678,
        "host": "localhost",
        "pathMappings": [
            {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "/myapp"
            }
        ]
    },

Point your web browser to http://localhost:5000/

You can make use of the following users:
- email `user@example.com` with password `Password1`.
- email `admin@example.com` with password `Password1`.


## Running the automated tests
    # Run pytest
    python -m pytest --setup-show --cov=app
 

## Trouble shooting
If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.


## Acknowledgements

With thanks to the following Flask extensions:

* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Script](https://flask-script.readthedocs.io/)

<!-- Please consider leaving this line. Thank you -->
[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.
  

## Authors

- Nicolas Hans (NHanser)