'''
test_models.py
'''

from unittest.mock import patch
from website.models import EmailData


# Helper to patch _is_massive_html for testing purposes: boolean returns
def dummy_is_massive_html_false(self, message, html_threshold, img_threshold):  # pylint: disable=unused-argument
    """
    Dummy method to always return False
    """
    return False


def dummy_is_massive_html_true(self, message, html_threshold, img_threshold):  # pylint: disable=unused-argument
    """
    Dummy method to always return False
    """
    return True


@patch("website.models.EmailData._is_massive_html", new=dummy_is_massive_html_false)
def test_email_data_init():
    '''
    GIVEN the EmailData class
    WHEN we initialize it with a subject and message
    THEN check that the subject and message are set correctly
    '''
    subject = "test subject"
    message = "test message"

    email_data = EmailData(subject, message)

    assert email_data.get_subject() == subject
    assert email_data.get_message() == message

    email_data_string = email_data.to_string()
    assert "START OF" in email_data_string
    assert subject in email_data_string


@patch("website.models.EmailData._is_massive_html", new=dummy_is_massive_html_true)
def test_email_data_init_htmloverflow():
    '''
    GIVEN the EmailData class
    WHEN we initialize it with a subject and message with too much html/img
    THEN check that the subject and message are set correctly
    '''
    subject = "test subject"
    message = "test message"

    email_data = EmailData(subject, message)

    assert email_data.get_subject() == subject
    assert "too many HTML" in email_data.get_message()
