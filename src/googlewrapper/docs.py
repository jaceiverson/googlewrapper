from .connect import Connection


class GoogleDocs:
    def __init__(self, doc_id = None) -> None:
        self.id = doc_id
        self.connection = Connection().docs()
        if doc_id:
            self.doc = self._get_doc()

    def set_id(self,doc_id:str):
        """Sets the ID to new ID, calls the API to get the new doc"""
        self.id = doc_id
        self.doc = self._get_doc()

    def _get_doc(self):
        """Returns the dictionary object of the Google Doc"""
        return self.connection.documents().get(documentId=self.id).execute()

    def get_title(self):
        """Returns the title of the Google Doc"""
        return self.doc.get('title')

    def get_id(self):
        """Returns the ID of the Google Doc"""
        return self.id

    def get_body(self):
        """Returns the Body of the Google Doc"""
        return self.doc.get('body')

    def combine_content(self,content:dict):
        """Accepts a dictionary from Google Docs, this will be a 
        list element from the body (self.get_body()) of the Google Doc
        
        returns the entire string from the content sections. This is the structure

        paragraph (one of the list elements of body, this is a dict) -> 
        elements (key in paragraph, list of dictionaries object) -> 
        textRun (key in each list object's variables of the elements list) -> 
        content (key in textRun, value contains the text values from the doc)
        
        """
        return ''.join([element['textRun']['content'].strip() for element in content['paragraph']['elements'] if 'pageBreak' not in element.keys()])

