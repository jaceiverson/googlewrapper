"""
Automate your weekly reporting using the template 
class and function below.

You can have this set to a cron job and 
have the output emailed or sent to a Google Sheet
"""
from googlewrapper import GoogleAnalytics
from googlewrapper import GoogleSearchConsole

import datetime as dt
import pandas as pd


class WeeklyReport:
    """
    Organic Weekly Report from GA and GSC
    """

    def __init__(
        self,
        week_start=dt.date.today() - dt.timedelta(days=8),
        week_end=dt.date.today() - dt.timedelta(days=2),
        output=True,
    ):
        # do you want to print the results out to console?
        # default True
        self.output = output

        # assign date range
        self.week_start = week_start
        self.week_end = week_end

        self.gsc_data = {}
        self.ga_data = pd.DataFrame()
        self.google_objects = {}

    def __print_dates(self):
        print(f"\n\n -- Data between {self.week_start} and {self.week_end} --\n")

    def process(self, view, site):

        ga = GoogleAnalytics(view)
        gsc = GoogleSearchConsole()

        if self.output:
            print(site)

        # GA
        ga_metrics = ["pageviews", "sessions"]
        ga.set_metrics(ga_metrics)
        ga_dims = ["channelGrouping"]
        ga.set_dimensions(ga_dims)
        # sets the GA to be organic traffic only
        organic_filter = [("channelGrouping", False, "EXACT", "Organic Search", True)]
        ga.set_dimension_filters(organic_filter)

        ga.set_start_date(self.week_start)
        ga.set_end_date(self.week_end)

        current_ga_data = ga.build_request()

        pageviews = current_ga_data["pageviews"].values[0]
        sessions = current_ga_data["sessions"].values[0]

        current_ga_data.index = [site]
        self.ga_data = self.ga_data.append(current_ga_data)

        # GSC
        gsc.set_sites([site])
        gsc.set_start_date(self.week_start)
        gsc.set_end_date(self.week_end)
        gsc.set_dimensions(["page"])

        current_gsc_data = gsc.get_data()

        clicks = current_gsc_data[site]["Clicks"].sum()
        impressions = current_gsc_data[site]["Impressions"].sum()
        position = current_gsc_data[site]["Position"].mean()

        current_gsc_data[site].index = current_gsc_data[site]["Page"]
        current_gsc_data[site].drop(columns="Page", inplace=True)
        self.gsc_data[site] = current_gsc_data[site]

        df = pd.DataFrame(
            data=[[pageviews, sessions, clicks, impressions, position]],
            columns=["pageviews", "sessions", "clicks", "impressions", "position"],
        )

        df["ctr"] = df["clicks"] / df["impressions"]

        df.index = [site]

        if self.output:
            print(f"{df}\n")

        self.google_objects[site] = {"GSC": gsc, "GA": ga}

        return df

    def from_dict(self, data):
        if self.output:
            self.__print_dates()
        # validate this is a dictionary
        if not isinstance(data, dict):
            raise TypeError("data needs to be a dictionary format")

        google_data = pd.DataFrame()
        # loop through the data and pull each of the points
        # if self.output == True, it will print to console
        # appends the results (pd.DataFrame) to a master DataFrame
        for key, value in data.items():
            google_data = google_data.append(self.process(value, key))
        # returns the created list for use
        return google_data


def monday_report_template(
    week_start=dt.date.today() - dt.timedelta(days=8),
    week_end=dt.date.today() - dt.timedelta(days=2),
):
    w = WeeklyReport(week_start, week_end)
    """
    Dictionary to be formated the following:
    keys: GSC property name
    values: GA View ID
    """
    my_site_data = {
        "sc-domain:example.com": "123456789",
        "https://www.othersite.com": "987654321",
    }
    return w.from_dict(my_site_data)


if __name__ == "__main__":
    report = monday_report_template()
