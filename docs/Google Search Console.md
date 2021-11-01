# Google Search Console
## Initialize 
```py
from googlewrapper import GoogleSearchConsole

gsc = GoogleSearchConsole()
```
## Methods

### Assigning Dates
The following all accept a datetime variable. By default the object will pull the last 7 days of data. There are 2 options for changing the date range to pull data for:

#### Option 1 - assign both start and end dates
> Use this option if you would like a range of dates
> 
>You need to call both these methods to assign start and end dates

```py
.set_start_date(start_date)
```
```py
.set_end_date(end_date)
```
#### Option 2 - assign one date
> Use this option if you only want to see one day worth of data
> 
> You only need to call the method below to make it work
```py
.set_date(date)
```
### Other GSC API Parameters
```py
.set_filters(filter_list)
```
Parameters
- filter_object: list of dictionaries
    - how to filter your GSC object
#### Example to get mobile data from the USA
```py
example_filter = [
                {
                "dimension": "device",
                "operator": "equals",
                "expression": "mobile"
                },
                {
                "dimension": "country",
                "operator": "equals",
                "expression": "usa"
                }
                ]

gsc.set_filters(example_filter)
```
#### More filter information
 - <a href=https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics/query#request-body target=_blank>See Google's Docs</a> for more details
 - metric filters are not assigned prior to the pull, filter data after the api pull
 - to reset (remove) filters call the method with an empty list ->  ```gsc.set_filters([])```

#### | Set GSC Dimensions
```py
.set_dimensions(dimensions)
```
Parameters
 - dimensions: list of dimension strings
    - all dimensions should remain in lowercase
    - Dimension String Options:
        - "page"
        - "query"
        - "date"
        - "country"
        - "device"
        - "searchAppearance"
 
 Default values: ```["page","date"]``` 

#### | Set Sites to Pull
```py
.set_sites(sites_list)
```
Parameters
 - sites_list: list
    - list of gsc properties (strings) we want to pull
    - domain properties should be prefaced with "sc-domain:" 
    - Example: ```["sc-domain:example.com"]```

Default values: ```self.all_sites()```

#### | Set Branded Queries
```py
.set_branded(branded_dictionary)
```
Parameters
 - branded_dictionary: dict
   - keys
      - GSC Property Name - Match exactly to GSC Portal
   - values
      - list of branded strings
         - if these values are found in any form in the query, marked as branded
        
Example:
```py
{'https://www.oreo.com':['oreo','nabisco','milks favorite cookie']}
```
If ```.set_branded()``` is not called, all queries will be marked as ```Branded = FALSE```


---
### Pulling Data
#### | Pull all properties from your authentication
```py
.all_sites(site_filter)
```
Parameters
 - site_filter: list of strings (optional)
    - will filter your sites to sites including the strings in the list
 
 **Returns**: list of all verified sites in the GSC profile
#### | Make the API call to return data
```py
.get_data()
```
- After assigning all the parameters - with the other class methods - run this method to make the api request
- This method does not accept any parameters

 **Returns**: dictionary object
   - Keys: Site URLs from the site_list
   - Values: pd.DataFrame of GSC data 
   - This dictionary object is also saved as the ```self.output``` attribute to use with ```self.ctr()```
#### | Get custom "Click Through Rates" for your GSC Property
```py
.ctr()
```
 - Calculates custom Click Through Rates based our our GSC data we pulled
 - For accurate results, make sure that you: 
   - have "query" in the dimension lis
   - have set branded queries using .set_branded()
 - This method does not accept any parameters

 **Returns**: dictionary object
   - Keys: ["all","branded","non-branded"]
   - Values: pd.DataFrame with index as Position and columns ["Clicks","Impressions","CTR"] 
   - This dictionary object is also saved as the ```self.my_ctr``` attribute to be referenced later

## Examples
### Pull one day's worth of data
```py
# initialize our class
from googlewrapper import GoogleSearchConsole
gsc = GoogleSearchConsole()

# assign variables to our GSC object
gsc.set_sites(sites_list)
gsc.set_date(dt.date.today())
gsc.set_dimensions(dim_list)

# call the api to get the data
data = gsc.get_data()
```
### Find Custom CTR for last 12 months
```py
# initialize our class
from googlewrapper import GoogleSearchConsole
gsc = GoogleSearchConsole()

#declare all the parameters
gsc.set_start_date(dt.date.today()-dt.timedelta(days=365))
gsc.set_end_date(dt.date.today())
gsc.set_dimensions(['query'])
gsc.set_branded(branded_dict)
gsc.set_sites(sites_list)

data = gsc.get_data()
ctr = gsc.ctr()
```
