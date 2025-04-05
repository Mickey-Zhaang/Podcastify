'''
gmail_summary.py
'''
import base64
from googleapiclient.discovery import build
from openai import OpenAI
from .models import EmailData


def build_service(creds):
    '''
    builds the Gmail API service
        returns: a service object for the Gmail API
    '''

    return build('gmail', 'v1', credentials=creds)

def list_past_message_ids(service):
    '''
    lists past messages from the user's Gmail account
        only returns a list of id's and thread id's
    '''
    results = service.users().messages().list(userId="me").execute()["messages"]

    return results

def get_top_k_messages(k, results, service):
    '''
    gets the top k messages from the user's Gmail account
        returns a list of message ids and thread ids
    '''
    # ChatGPTed
    def decode_base64_data(data_str):
        missing_padding = len(data_str) % 4
        if missing_padding:
            data_str += "=" * (4 - missing_padding)
        decoded_bytes = base64.urlsafe_b64decode(data_str.encode("utf-8"))
        return decoded_bytes.decode("utf-8", errors="replace")

    top_k_messages = results[:k] if len(results) > k else results
    message_ids = [message.get("id") for message in top_k_messages]

    res_messages = [service.users().messages().get(userId="me",
                                                   id=id,
                                                   format="full").execute().get("payload") for id in message_ids]

    top_k_emails = []
    for res in res_messages:
        subjects = next((header.get("value") for header in res.get("headers", []) if header.get("name") == "Subject"),
                        "No Subject")
        body = res.get("parts")[0].get("body").get("data")
        if body:
            body = decode_base64_data(body)
        else:
            body = "Nothing here"
        top_k_emails.append(EmailData(subjects, body))
    return top_k_emails

def podcastify(res_messages, api_key):
    '''
    processes the messages and returns a summary of each email
    '''

    client = OpenAI(api_key=api_key)

    user_input = [email.to_string() for email in res_messages]

    messages = [
    {
        "role": "system",
        "content": (
            "You are given a list of emails, each containing a SUBJECT and MESSAGE. "
            "For any emails that don't have a meaningful body, say so but address the SUBJECT"
            "Provide a single, concise, and engaging podcast summary "
            "that captures the key points of all understandable emails."
        )
    },
        {
            "role": "user",
            "content": str(user_input)
        }
    ]

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
    )
    return str(completion.choices[0].message.content)
