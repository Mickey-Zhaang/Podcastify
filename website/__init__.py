'''
Wesbite Factory: The Root
'''
import os
from dotenv import load_dotenv
from flask import Flask
from .views import main_blueprint
from .google_oauth import auth_blueprint

load_dotenv()

def create_app():
    '''
    Called by app.py to create a Flask App instance
    '''
    app = Flask(__name__)

    app.config["DEBUG"] = True
    app.secret_key = os.environ.get("SECRET_KEY", "a-very-secret-key")
    # API KEY STUFF
    app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
    # Google Oauth
    app.config["GOOGLE_CLIENT_ID_WEB"] = os.environ.get("GOOGLE_CLIENT_ID_WEB")
    app.config["GOOGLE_CLIENT_SECRET_WEB"] = os.environ.get("GOOGLE_CLIENT_SECRET_WEB")

    # register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
