# Google Analytics
## Initialize 
```py
from googlewrapper import GoogleAnalytics

ga = GoogleAnalytics()
```
## Methods
### Assigning Metrics & Dimensions
```py
.set_metrics()
```
```py
.set_dimensions()
```
Parameters
- metric/dimensions: list of strings
    - this are the metric and dimension names from Google Analytics
    
 Metric and Dimension names can be found on <a href=https://ga-dev-tools.web.app/dimensions-metrics-explorer/>Google Analytic's Dev Tools</a> site. In these methods, **DO NOT** include the "ga:" before the metrics or dimensions. The class assigns these automatically at run-time.

### Filtering Metrics & Dimensions
```py
.set_metric_filters()
```
```py
.set_dimension_filters()
```
Parameters
- filters: list of tuples
    - Each tuple is formated as follows:
```
# DIMENSION FILTER TUPLE
(dimension name, "not", operator, expression, caseSensitive)

# METRIC FILTER TUPLE
(metric name, "not", operator, comparisonValue)
```
|Filter Name|Description|Example|
|:-:|:-:|:-:|
|name|Which GA metric/dimension we want to filter on|"channelGrouping"|
|"not"|If we want to exclude these named values; False = Include, True = Exclue| False | 
|<a href = https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#operator>operator (dimensions)</a>| operator to compare dimension to; possible values below | "EXACT"|
|expression (dimensions)|Strings or regular expression to match/compare against|"Organic Search"|
|caseSenstitive (dimensions)| If dimension filters are case senstitive | True|
|<a href = https://developers.google.com/analytics/devguides/reporting/core/v4/rest/v4/reports/batchGet#operator_1>operator (metrics)</a> | operator to compare metric to; possible values below | "GREATER THAN" |
|comparisonValue (metrics)|Strings or regular expression to match/compare against|"100"|


#### Dimension Operator Possible Values
```["REGEXP","BEGINS_WITH","ENDS_WITH","PARTIAL","EXACT","NUMERIC_EQUAL","NUMERIC_GREATER_THAN", "NUMBER_LESS_THAN","IN_LIST"]```
#### Metric Operator Possible Values
```["EQUAL", "LESS_THAN","GREATER_THAN","IS_MISSION"]```
#### Example Dimension Filter List
```
dim_filter = [('channelGrouping',False,"EXACT","Organic Search",True),('landingPage',False,"BEGINS_WITH","/blog/")]
ga.set_dimension_filters(dim_filter)
ga.set_dimension_filter_group("AND")
```
This will filter Organic Search to the Blog

#### Example Metric Filter List
```
metric_filter = [('pageviews',False,"GREATER_THAN","1000")]
ga.set_metric_filter(metric_filter)
```
This will filter to only show pageviews > 1000

### Seting Filter Group Opperation (OR vs AND)
```py
.set_metric_filter_group()
```
```py
.set_dimension_filter_group()
```
Parameters
 - filter_group: str
    - accepts a string ("OR" or "AND"). 

This sets the logical operator to "OR" or "AND". This does not matter, if you only have less than 2 filter tuples in your filter list; however, it becomes very important one you have 2 or more filters applied.

Default value: ```"OR"```

### Setting Date Range
```py
.set_start_date()
```
```py
.set_end_date()
```
Parameters
 - start/end date: dt.datetime
    - these are inclusive dates 

### Pulling Data
```py
.build_request()
```
Once you have prepared your GA object with dimensions,metrics, filters, and date ranges, you can call this method to get your data. It will retrn a pd.DataFrame, but that can be changed by initializing your GA object with the attribute ```default_view = "dict"```
 - This method does not accept any parameters

## Examples
```py
# Initialize
from googlewrapper import GoogleAnalytics
ga = GoogleAnalytics()

# Assign Metrics
ga_metrics = ['pageviews','sessions']
ga.set_metrics(ga_metrics)

# Assign Dimensions
ga_dims = ['channelGrouping']
ga.set_dimensions(ga_dims)

# Set a Filter (organic only)
organic_filter_list = [('channelGrouping',False,"EXACT","Organic Search",True)]
ga.set_dimension_filters(organic_filter_list)

# Assign Start/End Dates
ga.set_start_date(self.start_date)
ga.set_end_date(self.end_date)

# Pull the data
ga_data = ga.build_request()
```
