from flask import Blueprint, redirect, render_template, flash, jsonify
from flask import request, url_for, session
from app.extensions import oauth, security, db
from flask_security import login_user
import datetime

blueprint = Blueprint('google', __name__)

#TODO : https://docs.authlib.org/en/v0.12.1/client/flask.html
"""@app.route('/google/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('account/verify_credentials.json')
    resp.raise_for_status()
    profile = resp.json()
    # do something with the token and profile
    return redirect('/')"""


@blueprint.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('google.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@blueprint.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    user_info = token.get('userinfo')  # userinfo contains stuff u specificed in the scope
    if not user_info:
        user_info = google.userinfo()
    if user_info["email_verified"]:
        unique_id = user_info["sub"]
        users_email = user_info["email"]
        picture = user_info["picture"]
        users_name = user_info["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # check if user exists
    security_user = security.datastore.find_user(email=user_info['email'])

    if security_user is None:
        # Create a user in your db with the information provided
        # by Google
        # inspired by https://realpython.com/flask-google-login/#openid-connect-details
        security_user = security.datastore.create_user(
                    email=users_email,
                    active=True,
                    confirmed_at=datetime.datetime.utcnow(),
                    registered_on = datetime.datetime.utcnow(),
                    current_login_at = datetime.datetime.utcnow(),
                    roles=['basic'])
        db.session.commit()
        
    # Begin user session by logging the user in
    login_user(security_user, remember=True, authn_via=["google-authenticator"])
    security.datastore.commit()
    return redirect('/')