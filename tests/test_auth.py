import pytest
from flask import g, session, url_for
from app.extensions import db
from app.users.models import User
from flask_security.utils import url_for_security


def test_register(myapp):
    assert myapp.test_client.get(url_for_security('register')).status_code == 200
    response = myapp.test_client.post(
        url_for_security('register'), data={'email': 'unittest@app.me', 'password': 'abcdefgh', 'password_confirm': 'abcdefgh'}
    )
    # check redirect to home_page
    assert response.headers["Location"] == url_for('core_bp.home_page', _external=False)
    users_ = db.session.query(User).all()
    assert db.session.query(User).filter_by(email='unittest@app.me').one() is not None


@pytest.mark.parametrize(('email', 'password', 'password_confirm', 'message'), (
    ('', '', '', b'Email not provided'),
    ('a', '', '', b'Invalid email address'),
    ('unittest@app.me', '', '', b'Password not provided'),
    ('unittest@app.me', 'a', '', b'Password must be at least 8 characters'),
    ('unittest@app.me', 'abcdefgh', '', b'Password not provided'),
    ('unittest@app.me', 'abcdefgh', 'abcdefg', b'Passwords do not match'),
    ('member@example.com', 'test', 'test', b'member@example.com is already associated with an account.'),
))
def test_register_validate_input(myapp, email, password, password_confirm, message):
    response = myapp.test_client.post(
        url_for_security('register'),
        data={'email': email, 'password': password, 'password_confirm': password_confirm}
    )
    assert message in response.data


def test_login(myapp):
    assert myapp.test_client.get(url_for_security('login')).status_code == 200
    response = myapp.test_client.post(
        url_for_security('login'), data={'email': 'member@example.com', 'password': 'Password1'}
    )
    # check redirect to home_page
    assert response.headers["Location"] == url_for('core_bp.home_page', _external=False)


@pytest.mark.parametrize(('email', 'password', 'messages'), (
    ('', '', [b'This field is required.', b'Password not provided']),
    ('unittest@app.me', '', b'Password not provided'),
    ('unittest@app.me', 'a', b'Specified user does not exist'),
    ('member@example.com', 'test',  b'Invalid password'),
))
def test_login_validate_input(myapp, email, password, messages):
    response = myapp.test_client.post(
        url_for_security('login'),
        data={'email': email, 'password': password}
    )
    if type(messages) != list:
        messages = [messages]
    for message in messages:
        assert message in response.data