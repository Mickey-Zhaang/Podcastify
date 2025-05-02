'''
testing the gmail_summary module
'''

from unittest.mock import MagicMock
from website.gmail_summary import build_service, list_past_message_ids, get_top_k_messages, podcastify
from website.models import EmailData


def test_build_service(monkeypatch):
    '''
    test's build_service from gmail_summary.py
    '''
    dummy_service = object()

    # Arbitrarily patches the parameters of build()
    monkeypatch.setattr("website.gmail_summary.build", lambda gmail, v1, credentials=None: dummy_service)
    creds = {"token": "token"}
    result = build_service(creds)

    assert result == dummy_service


def test_list_past_message_ids():
    '''
    tests list_past_message_ids
    '''
    expected = [{"id": "1", "threadId": "t1"}]
    service = MagicMock()
    service.users().messages().list().execute.return_value = {"messages": expected}

    result = list_past_message_ids(service)

    assert result == expected


def test_get_top_k_messages():
    '''
    test get_top_k_messages
    '''
    res_messages = {"headers": [{"name": "Subject", "value": "Testing Subject"}], "body": {"data": "VGVzdGluZyBEYXRh"}}
    results = [{"id": 1, "1message": "1testing"}]
    service = MagicMock()
    service.users().messages().get.return_value.execute.return_value.get.return_value = res_messages

    resp = get_top_k_messages(1, results, service)
    resp = resp[0]
    assert resp.get_subject() == "Testing Subject"
    assert resp.get_message() == "Testing Data"


# def test_podcastify():
#     '''
#     tests podcastify
#     '''
#     res_messages = [EmailData("Testing Subject", "test 1")]

#     dummy_response = MagicMock()
#     dummy_response.choices = [MagicMock(message=MagicMock(content="Here's the Podcast"))]

#     dummy_chat = MagicMock()
#     dummy_chat.completion.create.return_value = dummy_response

#     dummy_client = MagicMock()
#     dummy_client.chat = dummy_chat
