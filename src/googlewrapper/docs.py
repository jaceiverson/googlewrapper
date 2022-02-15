from googlewrapper.connect import Connection
from typing import Optional


class GoogleDocs:
    def __init__(self, doc_id: Optional[str] = None) -> None:
        self.id = doc_id
        # authentication
        self.connection = self.__auth()
        # if there is an ID, we will pull the document object
        if doc_id:
            self.doc = self._get_doc()

    def __str__(self):
        if self.doc:
            return self.get_title()
        return self

    def __repr__(self):
        return self.__str__()

    def __auth(self):
        """Authenticates to Google"""
        return Connection().docs()

    def set_id(self, doc_id: str) -> None:
        """Sets the ID to new ID, calls the API to get the new doc"""
        self.id = doc_id
        self.doc: dict = self._get_doc()

    def _get_doc(self) -> dict:
        """Returns the dictionary object of the Google Doc"""
        return self.connection.documents().get(documentId=self.id).execute()

    def get_title(self) -> str:
        """Returns the title of the Google Doc"""
        return self.doc.get("title")

    def get_id(self) -> str:
        """Returns the ID of the Google Doc"""
        return self.id

    def get_header(self) -> list[dict]:
        """Returns the Header of the Google Doc"""
        return (
            self.doc.get("headers")
            .get(list(self.doc.get("headers").keys())[0])
            .get("content")
        )

    def get_body(self) -> list[dict]:
        """Returns the Body of the Google Doc"""
        return self.doc.get("body").get("content")

    def get_text(self, doc_object: list[dict]) -> str:
        """
        Returns the text values of the entire document body as a string
        It is reccomended that you pass in

            self.get_header() or self.get_body()

        as the doc_object for best results
        """
        return "\n".join(
            [self.combine_content(x) for x in doc_object if "paragraph" in x.keys()]
        )

    def combine_content(self, content: dict) -> str:
        """Accepts a dictionary from Google Docs, this will be a
        list element from the body (self.get_body()) of the Google Doc

        returns the entire string from the content sections. This is the structure

        paragraph (one of the list elements of body, this is a dict) ->
        elements (key in paragraph, list of dictionaries object) ->
        textRun (key in each list object's variables of the elements list) ->
        content (key in textRun, value contains the text values from the doc)

        """
        return "".join(
            [
                element["textRun"]["content"]
                for element in content["paragraph"]["elements"]
                if "pageBreak" not in element.keys() and "textRun" in element.keys()
            ]
        ).strip()
