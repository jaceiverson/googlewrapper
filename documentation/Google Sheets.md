# Google Sheets
To initialize, you need to pass in the URL of the sheet you wish to use. By default the first sheet is set to the active sheet, but that can be changed by calling 
`.set_tab(new_sheet_name)`
## Initialize 
```py
from googlewrapper import GoogleSheets

gs = GoogleSheets(YOUR_URL_HERE)
```
## Methods
```py
.set_tab(sheet_name)
```
Assign which tab we will be pulling from. This must be called to make the other methods work properly.

Parameters
- sheet_name: str
    - the name of the tabe we want to pull from
---
```
.get_df(start='a1',index=1)
```
pulls the google sheet and returns it as a pd.DF

Parameters
 - start (optional)
    -  where we want the top left (including headers) of our table to start
    - defaults to 'a1'
- index (optional)
    - which column will be the index when pulled
    - defaults to the first column
---
```py
.save(df,start = 'a1',index=True,header=True,extend=True))
```
Saves a pd.DF to our assigned GoogleSheet

Parameters
- df: pandas.DataFrame
    - data we want to save
- start: str (optional)
    - where we want to start saving the data
    - default: 'a1'
- index: bool (optional)
    - include the pd.DF index in the sheet
    - default: True
- header: bool (optional)
    - include the headers in the sheet?
    - default: True
- extend: bool (optional)
    - if rows/columns would be cut off, create those rows/columns and place the data
    - default: True
---
```
.clear(start,end)
```
Removes any data from the selected range of cells. Does not remove formatting

Parameters
- start: str
    - formatted as cell reference
    - top left cell to start clearing
- end: str
    - formatted as cell reference
    - bottom right cell to end clearing
---

```
.row(row_number)
```
Returns an entire row of data.

Parameters
- row_number: int
    - which row number you want to pull
---

```
.col(col)
```
Returns an entire column of data.

Parameters
- col_number: int
    - which column number you want to pull
---
```
.add_tab(sheet_name,data=None)
```
Creates a new sheet/tab in your spreadsheet. Assigns that sheet as the active sheet - _self.set_sheet()_. If you pass in data (a pd.DF), it will also write that data starting in 'a1' of your new tab. 

Parameters
- sheet_name: str
    - the name of the new tab to be created
- data: pandas.DataFrame
    - data that you want filled in to 'a1' on the new tab
---
```
.delete_tab(sheet_name)
```
Deletes the sheet/tab whose name you pass in.
Parameters
- sheet: str
    - which tab you would like to delete
---
```
.share(email_list,role = 'reader')
```
Shares your spreadsheet with all emails in the list. Can assign different permissions. 

Parameters
- email_list: list
    - all the emails you'd like to share this with
- role: str
    - which permissions to grant this email list
    - options: 'reader','commenter','editor'
