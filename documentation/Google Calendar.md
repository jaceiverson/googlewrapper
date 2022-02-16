# Google Calendar
## Initialize 
```py
from googlewrapper import GoogleCalendar

cal = GoogleCalendar()
```
## Methods
```py
.set_default(cal_id)
```
 - Assigns which calendar will be used to create and find events
---
```py
.find_event(str)
```
   - Searches for an event in your calendar by name 
   - Returns <a href=https://developers.google.com/calendar/v3/reference/events/list#response>events list response object</a>
---
```py
.get_event(eventId)
```
Returns the <a href=https://developers.google.com/calendar/v3/reference/events#resource>event object</a> of the eventId you passed in

---
```py
.all_events(num_events,min_date)
```
Parameters
- num_events: int
    - Number of events you'd like to return
    - defaults to 250
- min_date: dt.datetime
    - starting point will only search forward in time from this date
    - defaults to the current date and time 

**Returns**: <a href=https://developers.google.com/calendar/v3/reference/events/list#response>events list response object</a>

---
```py
.update_event(new_event,send_updates)
```
Parameters
  - new_event: dict
    - event formatted json to update
  - send_updates: str
    - if you want to send the updates
    - see <a href=https://developers.google.com/calendar/v3/reference/events/update#parameters>Google's Docs</a> for more info
    - defaults to 'all'

**Returns**: <a href=https://developers.google.com/calendar/v3/reference/events#resource>updated event object</a>

## Examples 
```py
my_event = cal.find_event('Team Meeting')
```
