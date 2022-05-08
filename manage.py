"""This file sets up a command line manager.

Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server on localhost:5000.
Use "python manage.py runserver --help" for a list of runserver options.
"""
from flask.cli import FlaskGroup

from app import create_app

# Setup Flask-Cli
app = create_app()
cli = FlaskGroup(create_app=app)

if __name__ == "__main__":
    # python manage.py                      # shows available commands
    # python manage.py runserver --help     # shows available runserver options
    app.run()
