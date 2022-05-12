from flask import Blueprint, redirect, render_template, flash, jsonify
from flask import request, url_for
from app.extensions import oauth

google_blueprint = Blueprint('main', __name__, template_folder='templates',
    static_folder='static')

#TODO : https://docs.authlib.org/en/v0.12.1/client/flask.html
@app.route('/google/login')
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
    return redirect('/')