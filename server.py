from flask import Flask, request, render_template, url_for, redirect, session
from os import environ as env
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

		
app = Flask(__name__)
app.secret_key = env['FLASK_SECRET']

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/")
def homepage():
	return render_template('home.html', home=True)

@app.route('/login', methods=['GET'])
def login():
	return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("homepage", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
@app.route("/seeUser")
def seeUser():
	user = session['user'] if 'user' in session else "No User"
	name = 'Guest'
	pic_url = ''
	if user != "No User":
		print(user)
		name = user['userinfo']['given_name']
		pic_url = user['userinfo']['picture']
	return render_template('seeUser.html', user=user, name=name, pic_url=pic_url) 