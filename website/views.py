'''
views.py
'''
import os
from google.oauth2.credentials import Credentials
from flask import Blueprint, render_template, session, redirect, url_for
from .gmail_summary import build_service, list_past_message_ids, get_top_k_messages, podcastify

main_blueprint = Blueprint("main", __name__)

@main_blueprint.route('/')
def index():
    '''
    Landing Page
    '''
    return render_template('index.html')

@main_blueprint.route('/start-process', methods=['POST'])
def start_process():
    '''
    Processing in Landing page
    '''
    if "credentials" not in session:
        return redirect(url_for('auth.auth'))
    creds = session.get("credentials")
    credientials = Credentials(**creds)
    service = build_service(credientials)
    past_messages_ids = list_past_message_ids(service)
    top_k_messages = get_top_k_messages(10, past_messages_ids, service)

    api_key = os.getenv("OPENAI_API_KEY")
    podcast = podcastify(top_k_messages, api_key)

    return render_template('index.html', podcast=podcast)
