"""
google oauth file
"""

import os
from flask import request, session, redirect, Blueprint
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import google.auth.transport.requests
import requests
from dotenv import load_dotenv

auth_blueprint = Blueprint("auth", __name__)
load_dotenv()


def create_flow():
    """
    creates a flow object
    """
    # web based: for heroku deployment
    web_redirect = "https://zhangpodcastify-5e7788df03d9.herokuapp.com/callback"
    # for local testing
    local_redirect = "http://localhost:5000/callback"

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID_WEB"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET_WEB"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [web_redirect, local_redirect],
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
            "https://www.googleapis.com/auth/gmail.readonly",
        ],
        redirect_uri=web_redirect,
    )
    return flow


def get_redirect_url():
    """
    gets the redirect URL for Google OAuth
        returns: dict with authorization URL and state
    """
    flow = create_flow()
    authorization_url, state = flow.authorization_url()
    return {"auth_url": authorization_url, "state": state}


@auth_blueprint.route("/auth")
def auth():
    """
    temporary to test
    """
    redirect_url = get_redirect_url()
    session["state"] = redirect_url["state"]
    return redirect(redirect_url["auth_url"])


@auth_blueprint.route("/callback")
def callback():
    """
    performs a callback
    """
    flow = create_flow()

    google_client_id = os.environ.get("GOOGLE_CLIENT_ID_WEB")
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token, request=token_request, audience=google_client_id
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return redirect("/")
