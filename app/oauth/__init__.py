from .google import blueprint as google_blueprint

# based on https://github.com/authlib/demo-oauth-client/blob/master/flask-multiple-login/app.py
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
def oauth_registration(oauth):
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    oauth.register(
        name='twitter',
        api_base_url='https://api.twitter.com/1.1/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        userinfo_endpoint='account/verify_credentials.json?include_email=true&skip_status=true',
        userinfo_compliance_fix=normalize_twitter_userinfo,
        fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
    )

def normalize_twitter_userinfo(client, data):
    # make twitter account data into UserInfo format
    params = {
        'sub': data['id_str'],
        'name': data['name'],
        'email': data.get('email'),
        'locale': data.get('lang'),
        'picture': data.get('profile_image_url_https'),
        'preferred_username': data.get('screen_name'),
    }
    username = params['preferred_username']
    if username:
        params['profile'] = 'https://twitter.com/{}'.format(username)
    return params


