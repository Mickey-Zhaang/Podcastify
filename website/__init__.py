'''
Wesbite Factory: The Root
'''
import os
from dotenv import load_dotenv
from flask import Flask
from .views import main_blueprint

load_dotenv()

def create_app():
    '''
    Called by app.py to create a Flask App instance
    '''
    app = Flask(__name__)

    app.config["DEBUG"] = True
    # API KEY STUFF
    app.config["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
    # Google Oauth
    app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID")
    app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET")

    # register blueprints
    app.register_blueprint(main_blueprint)

    return app
