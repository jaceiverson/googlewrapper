"""API Wrapper for Google Calendar"""

import datetime as dt
from typing import Optional, Any

from .connect import Connection


class GoogleCalendar:
    """
    Calender Wrapper Class
    REMEMBER your 'client_secret.json' file in your PATH

    Parameters
    cal_id: string id of calendar in Google Calendar
            This is found in your calendar settings
    """

    def __init__(self, cal_id: Optional[str] = None):

        self.service = Connection().cal()

        # pulls all calendars your authentication has access to
        # saves as self.cal_list
        self.cal_list: dict[Any, Any] = {}
        self.__all_calendars()

        # if not passed in as parameter, console will prompt for
        # calendar id to be inputed
        self.cal_id = cal_id
        if cal_id is None:
            self.set_calendar()

    def __all_calendars(self) -> None:
        """
        sets the self.cal_list variable to all the calendars
        that this authentication of google has access to

        you can see these by calling self._print_ids()
        """
        self.cal_list = self.service.calendarList().list().execute()

    def _print_ids(self, data: dict[Any, Any] = {}) -> None:
        """
        prints the ids of a calendar event, or calendar list
        defaults to printing the calendar list

        used when setting up the default calendar
        """
        if not data:
            data = self.cal_list

        for event in data["items"]:
            try:
                print(f"Name: {event['summary']}, ID: {event['id']}")
            except ValueError:
                print(f"Error with {event}")

    def set_calendar(
        self, hide_prompt: bool = False, cal_id: Optional[str] = None
    ) -> None:
        """
        allows you to set a default (active) calendar

        will print a list of all calendars for your account
        then prompt you to enter the calendar id in console

        prompt can be silenced by calling this function with
        the hide_prompt parameter set to True

        """
        if hide_prompt:
            if cal_id is None:
                raise ValueError(
                    "Please pass in your calendar ID "
                    "if silencing the console prompt. "
                    'cal_id = "your_cal_id"'
                )
            self.cal_id = cal_id
        else:
            self._print_ids()
            self.cal_id = input("\nType ID of calendar: ")

    def find_event(self, name: str) -> dict[Any, Any]:
        """
        search for an event by the event title (name)

        returns a event list dictionary object of all events found
        """
        event: dict[Any, Any] = (
            self.service.events().list(calendarId=self.cal_id, q=name).execute()
        )
        return event

    def get_event(self, event_id: str) -> dict[Any, Any]:
        """
        query calendar for an event by the event id (event_id)

        returns a event dictionary object of the event id
        """
        event: dict[Any, Any] = (
            self.service.events()
            .get(calendarId=self.cal_id, eventId=event_id)
            .execute()
        )
        return event

    def all_events(
        self,
        num_events: int = 100,
        min_date: str = dt.date.today().strftime("%Y-%m-%dT%H:%M:%SZ"),
    ):
        """
        returns all events on a calendar

        defaults to only 100 events, but that can be changed
        up to 2500 using the num_events parameter

        min_date parameter is the date/time time which the search starts

        returns the dictionary with events in a list
        under the dictionary['items']
        """
        return (
            self.service.events()
            .list(calendarId=self.cal_id, maxResults=num_events, timeMin=min_date)
            .execute()
        )

    def update_event(
        self, new_event: dict[Any, Any], send_update: str = "all"
    ) -> dict[Any, Any]:
        """
        updates an event on your calendar

        accepts the updated dictionary object (new_event)
        uses the 'id' field from new_event to update your calendar

        option to send updates to invites is default yes
        can be changed to 'none', or 'externalOnly'

        returns the updated event dictionary
        """
        updated_event: dict[Any, Any] = (
            self.service.events()
            .update(
                calendarId=self.cal_id,
                eventId=new_event["id"],
                body=new_event,
                sendUpdates=send_update,
            )
            .execute()
        )
        return updated_event
