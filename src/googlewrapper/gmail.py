"""
take inspiration from this class in python 2 that converts the byte objects into a pandas df

https://github.com/robertdavidwest/google_api/blob/master/google_api/gmail.py

CHANGES
Use my connection module
Us BytesIO instead of StringIO (converted from p2)
More comments, type hints and docs
Be able to send stuff it important too

"""
import pandas as pd

from .connect import Connection


class Gmail:
    def __init__(self) -> None:
        self.auth = self.__auth()

    def __auth(self):
        """returns googleapi.discovery build() Resource object for interacting with Gmail"""
        return Connection.gmail()

    def __str__(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return self.__str__()

    def build_message_body(
        self,
        message_id,
        thread_id,
        label_id,
        snippet,
        history,
        internal_date,
        payload,
        size,
    ) -> dict:
        """
        build the message body to send
        https://developers.google.com/gmail/api/reference/rest/v1/users.messages#Message
        """
        base_message = {
            "id": message_id,
            "threadId": thread_id,
            "labelIds": [label_id],
            "snippet": snippet,
            "historyId": history,
            "internalDate": internal_date,
            "payload": {payload},
            "sizeEstimate": size,
        }

    def get_message(self, message_id: str) -> dict:
        """return the dictionary value of a message given the id"""
        pass

    def send_message(
        self,
    ):
        pass
