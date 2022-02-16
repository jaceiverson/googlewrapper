# Google Docs
## Initialize 
```py
from googlewrapper import GoogleDocs

doc = GoogleDocs(doc_id)
```
It is prefered to initialize with the document id, but is not required. 
## Methods
```py
.set_id(doc_id)
```
Used to set/change the ID of the current Google Document
* doc_id is a string
No Return
```py
.get_title()
```
Returns the string value of the name of the Google Doc
```py
.get_id()
```
Returns the string id of the Google Doc
```py
.get_header()
```
Returns the header object of the Google Doc. This is a dictionary object. It is reccomended to use this method with the ```self.get_text()``` method to get textual values.
```py
.get_body()
```
Returns the body object of the Google Doc. This is a dictionary object. It is reccomended to use this method with the ```self.get_text()``` method to get textual values.
```py
.get_text(doc_object)
```
Returns a string of all text in the body/header.
doc_object is the dictionary value from ```.get_header()``` or ```.get_body()```.
## Examples 