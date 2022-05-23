# Copyright 2019 by J. Christopher Wagner (jwag). All rights reserved.

from unittest.mock import Mock
import pytest


from .utils import WrapApp
from app import create_app
from app.extensions import db as _db

from app.users.models import User, Role
from app.commands import find_or_create_role, find_or_create_user

#app = create_app(dict(
#    TESTING=True,  # Propagate exceptions
#    LOGIN_DISABLED=False,  # Enable @register_required
#    MAIL_SUPPRESS_SEND=True,  # Disable Flask-Mail send
#    SERVER_NAME='localhost',  # Enable url_for() without request context
#    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory SQLite DB
#    WTF_CSRF_ENABLED=False,  # Disable CSRF form validation
#    SECURITY_EMAIL_VALIDATOR_ARGS={ "check_deliverability": False}, # Our test emails/domain isn't necessarily valid
#    SECURITY_PASSWORD_HASH="plaintext", # Make this plaintext for most tests - reduces unit test time by 50%
#    SECURITY_SEND_REGISTER_EMAIL=False
#))

#app.app_context().push()



#bmock = Mock()
#app.blog_cls = bmock

# Create only one app to avoid blueprints conflicts while running multiple tests in one test file
#my_app = WrapApp(app, User, Role) #, mocks={"blog_mock": bmock}"""

#@pytest.fixture
#def myapp():
#    return my_app    
    

#@pytest.fixture
#def client(myapp):
#    return myapp.test_client()


@pytest.fixture(scope='session')
def app(request):
    """An application for the tests."""
    app = create_app(dict(
        TESTING=True,  # Propagate exceptions
        LOGIN_DISABLED=False,  # Enable @register_required
        MAIL_SUPPRESS_SEND=True,  # Disable Flask-Mail send
        SERVER_NAME='localhost',  # Enable url_for() without request context
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory SQLite DB
        WTF_CSRF_ENABLED=False,  # Disable CSRF form validation
        SECURITY_EMAIL_VALIDATOR_ARGS={ "check_deliverability": False}, # Our test emails/domain isn't necessarily valid
        SECURITY_PASSWORD_HASH="plaintext", # Make this plaintext for most tests - reduces unit test time by 50%
        SECURITY_SEND_REGISTER_EMAIL=False
    ))
    app.user_cls = User
    app.role_cls = Role
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    yield app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', 'Admin')
    basic_role = find_or_create_role('basic', 'Basic')

    # Add users
    user = find_or_create_user('admin@example.com', 'Password1', admin_role)
    user = find_or_create_user('member@example.com', 'Password1', basic_role)

    # Save to DB
    _db.session.commit()

    assert _db.session

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

@pytest.fixture
def client(app, session):
    return app.test_client()