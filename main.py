from flask import Flask, render_template, session, request
from google.cloud import datastore
from google.oauth2 import id_token
from requests_oauthlib import OAuth2Session
from google.auth.transport import requests

import boats
import users
import loads
import constants

# This disables the requirement to use HTTPS so that you can test locally.
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.register_blueprint(boats.bp)
app.register_blueprint(users.bp)
app.register_blueprint(loads.bp)

app.secret_key = os.urandom(24)
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

client = datastore.Client()
client_id = '155864832310-rqqbf4p2d9pjgf2qttitn62h4duun8oh.apps.googleusercontent.com'
client_secret = "xeCqwxUqsKTZa2pmyKfFeTnL"

redirect_uri = 'http://127.0.0.1:8080/oauth'

scope = ['https://www.googleapis.com/auth/userinfo.email',
         'https://www.googleapis.com/auth/userinfo.profile']

oauth = OAuth2Session(client_id,
                      redirect_uri=redirect_uri,
                      scope=scope)


@app.route('/')
def home():
    return render_template('login/welcome.html')


@app.route('/userLogin')
def user_login():
    return index()


def index():
    authorization_url, state = oauth.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        # access_type and prompt are Google specific extra
        # parameters.
        access_type="offline", prompt="select_account")
    return 'Please go <a href=%s>here</a> and authorize access.' % authorization_url


# This is where users will be redirected back to and where you can collect
# the JWT for use in future requests
@app.route('/oauth')
def oauthroute():
    token = oauth.fetch_token(
        'https://accounts.google.com/o/oauth2/token',
        authorization_response=request.url,
        client_secret=client_secret)

    req = requests.Request()

    id_info = id_token.verify_oauth2_token(
        token['id_token'], req, client_id)

    found_user = False

    query = client.query(kind=constants.users)
    query_iter = query.fetch()

    new_users = datastore.entity.Entity(key=client.key(constants.users))

    new_users.update({"JWT": token['id_token'],
                      "Unique ID": id_info['sub']})

    for entity in query_iter:
        if entity['Unique ID'] == id_info['sub']:
            found_user = True

            users_result = {"Unique ID": id_info['sub'],
                            "JWT": token['id_token']}

    if not found_user:

        client.put(new_users)

        users_result = {"Unique ID": id_info['sub'],
                        "JWT": token['id_token']}

    return render_template('/login/user_info.html', issued_JWT=token['id_token'], issued_id=users_result["Unique ID"])


# This page demonstrates verifying a JWT. id_info['email'] contains
# the user's email address and can be used to identify them
# this is the code that could prefix any API call that needs to be
# tied to a specific user by checking that the email in the verified
# JWT matches the email associated to the resource being accessed.
@app.route('/verify-jwt')
def verify():
    req = requests.Request()

    id_info = id_token.verify_oauth2_token(
        request.args['jwt'], req, client_id)

    return repr(id_info) + "<br><br> the user is: " + id_info['email']


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
