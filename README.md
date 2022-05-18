# googlewrapper

[![PyPI Latest Release](https://img.shields.io/pypi/v/googlewrapper.svg)](https://pypi.org/project/googlewrapper/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


General Connector Classes for Google Products 

__Current Wrappers Available__

 - <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Google%20Analytics.md>Google Analytics</a>
 - <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Google%20Search%20Console.md>Google Search Console</a>
 - <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Google%20Calendar.md>Google Calendar</a>
 - <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Google%20Big%20Query.md>Google Big Query</a>
 - <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Pagespeed%20Insights.md>Google PageSpeed API</a>
 - <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Google%20Sheets.md>Google Sheets</a>
 - <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Google%20Docs.md>Google Docs</a>

_Wrappers In the Pipeline_
- <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Gmail.md>Gmail</a>
- Google Maps  

# STEPS
 1) <a href=https://github.com/jaceiverson/googlewrapper#Acquire-Google-Credentials-from-API-Console>Acquire Google Credentials from API Console</a>
 2) <a href=https://github.com/jaceiverson/googlewrapper#installation>Install this package</a>
 3) <a href=https://github.com/jaceiverson/googlewrapper/blob/master/documentation/Google%20Authentication.md>Create Connection in Python</a>
 4) Use product wrapper to make API calls (see links to individual docs above)

## Acquire Google Credentials from API Console
First we will need to get our own Google Project set up so we can get our credentials. If you don't have experience, you can do so here <a href=https://console.cloud.google.com/apis/dashboard>Google API Console</a>

After you have your project set up, oAuth configured, and the optional service account (only for Google Big Query connections), you are good to install this package.

Make sure to download your oAuth credentials and save them to your working directory as 'client_secret.json'.

## Installation
### Create virtual enviornment
I recommended to create a virtualenv using the <a href="https://pypi.org/project/virtualenv/" target="_blank">virtualenv library</a>. Follow these steps:

#### install the package to main python instance
```
pip3 install virtualenv
```
#### actually create the virtual enviornment
```
python3 -m virtualenv venv
```
#### activate the enviornment
```
source venv/bin/activate
```
Now we can install the module:
```
pip install googlewrapper
```
OR
```
python -m pip install googlewrapper
```
#### general use for virtual environments
It is recommended to use virtualenvs when working with python and storing all your dependencies in a `requirements.txt` file. When you do that, you can simply install all the necessary packages by running the command
```
pip install requirements.txt -r
```
This will attempt to install everything in that text file. Normally packages will include dependency installs automatically. For example, when you run `pip install googlewrapper` all the dependencies (and unfortuneately there are quite a few) will automatically be installed. 

## Combining Products Examples
### Example 1
> Take a list of URLs from Sheets, grab Search Console Data, and import it into Big Query.

```py
from googlewrapper import GoogleSearchConsole, GoogleSheets, GoogleBigQuery
import datetime as dt

# init our objects
sheets = GoogleSheets(YOUR_URL_HERE)
gsc = GoogleSearchConsole()
gbq = GoogleBigQuery()

# get our urls we want to pull
# remember that sheet1 is default
sites = sheets.get_column(1)

'''
this one is a bit more technical
we can pull our column Branded Words right 
from sheets then assign it to a dictionary to use
in our GSC object.

Make sure that your url column is the index for 
your df. This will happen by default if the urls
are in the first column in google sheets
'''
branded_list = sheets.df()['Branded Words'].to_dict()

# assign those sheets to GSC
gsc.set_sites(sites)
# assign other GSC variables
gsc.set_date(dt.date(2021,1,1))
gsc.set_dims(['page','date','query'])

# get our data
gsc_data = gsc.get_data()

# print the total clicks/impressions and avg position
# for all the sites we just pulled data for
# send them to Big Query
for site in gsc_data:
  print(f"{site}'s Data\n"\
      f"Clicks: {gsc_data[site]['Clicks'].sum()}\n"\
      f"Impressions: {gsc_data[site]['Impressions'].sum()}\n"\
      f"Avg Position: {gsc_data[site]['Position'].mean()}\n\n")
  # now we will send our data into our GBQ tables for storage
  # we will assign the dataset name to be our url
  # we will assign table to be gsc
  gbq.set_dataset(site)
  gbq.set_table('gsc')
  # send the data to GBQ
  gbq.send(gsc_data[site])
```

## Thanks for using my code
<p align="center">
If you found this library useful, I'd appreciate a coffee. Thanks.
<br>
<br>
<a href="https://www.buymeacoffee.com/jaceiverson" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
</p>
