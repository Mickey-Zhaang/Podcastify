'''
models.py: holds data classes
'''
from bs4 import BeautifulSoup

class EmailData:
    '''
    a way to parse and store email data
    '''
    def __init__(self, subject, message, html_tag_threshold=100, img_tag_threshold=10):
        """
        Initialize an EmailData instance. Optionally, filter out messages
        that contain too many HTML or image tags.
        """
        self.subject = subject
        # Filter the message if it appears to be "massive" in HTML content.
        if self._is_massive_html(message, html_tag_threshold, img_tag_threshold):
            self.message = "[Filtered: Message contains too many HTML elements or images]"
        else:
            self.message = message

    def _is_massive_html(self, message, html_threshold, img_threshold):
        """
        Check if a message has too many HTML tags or <img> tags.
        Returns True if the message exceeds the thresholds.
        """
        # Parse the message as HTML. If it's plain text, BeautifulSoup will have few tags.
        soup = BeautifulSoup(message, "html.parser")

        # Count all HTML tags
        html_tags = soup.find_all()
        # Count <img> tags specifically
        img_tags = soup.find_all('img')

        if len(html_tags) > html_threshold or len(img_tags) > img_threshold:
            return True
        return False

    def get_subject(self):
        '''
        gettr for subject
        '''
        return self.subject

    def get_message(self):
        '''
        gettr for message
        '''
        return self.message

    def to_string(self):
        '''
        to_string method for EmailData
        '''
        return f">>>>>>>START OF '{self.subject}' Email <<<<<<<\nSUBJECT: {self.subject} \nMESSAGE: {self.message}\n >>>>>>>END OF '{self.subject}' Email <<<<<<<" # pylint: disable=line-too-long
