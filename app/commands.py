# This file defines command line commands for manage.py

import datetime

from app.extensions import db, security
from app.models.feedeater_models import Feed
from app.models.user import User, Role

from flask import Blueprint
from flask import current_app as app
import click
from werkzeug.security import generate_password_hash, check_password_hash


# Blueprint Configuration
commands_bp = Blueprint(
    'init', __name__
)

@commands_bp.cli.command()
@click.option('-d', '--delete', is_flag=True, default=False, is_eager=True)
def init_db(delete):
    """ Initialize the database."""
    if delete:
        print("Deleting database content")
        db.drop_all()
    db.create_all()


@commands_bp.cli.command()
def create_feeds():
    feed = Feed(
        title='Real Python', status=1, url='https://realpython.com/atom.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed)
    feed2 = Feed(
        title='Planet Python', status=1, url='http://planetpython.org/rss20.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed2)
    feed3 = Feed(
        title="Simon Willison's Weblog", url='https://simonwillison.net/atom/everything/', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow()
    )
    db.session.add(feed3)
    feed4 = Feed(
        title="Django community", url='https://www.djangoproject.com/rss/community/blogs/', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed4)
    feed5 = Feed(
        title="PyCharm Blog", url='http://feeds.feedburner.com/Pycharm', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed5)
    feed6 = Feed(
        title="The Django weblog",	url='https://www.djangoproject.com/rss/weblog/', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed6)
    feed7 = Feed(
        title="SQLAlchemy", url='https://www.sqlalchemy.org/blog/feed/atom/index.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed7)
    feed8 = Feed(
        title="Blog — Pallets Project", url='http://www.palletsprojects.com/blog/feed.xml', type='rss',
        created=datetime.datetime.utcnow(), updated=datetime.datetime.utcnow())
    db.session.add(feed8)

    db.session.commit()

@commands_bp.cli.command()
def create_users():
    """ Create users """
    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', 'Admin')

    # Add users
    user = find_or_create_user('admin@example.com', 'admin', 'Admin', 'Example', 'Password1', admin_role)
    user = find_or_create_user('member@example.com', 'member', 'Member', 'Example', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, description):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, description=description)
        db.session.add(role)
    return role


def find_or_create_user(email, username, first_name, last_name, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.username == username).first()
    if not user:
        new_user = security.datastore.create_user(email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=generate_password_hash(password),
                    active=True,
                    confirmed_at=datetime.datetime.utcnow())
        
        if role:
            new_user.roles.append(role)
    return user


