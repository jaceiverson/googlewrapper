"""Create a report comparing 2 periods in GSC"""

import datetime as dt
from typing import Optional

from dateutil.relativedelta import relativedelta
import pandas as pd

from googlewrapper import GoogleSearchConsole, GoogleSheets
from pdcompare import Compare


def _get_historical_months(months_back: int = 1) -> tuple:
    """
    takes in an int representing the number of months you want to go back
    defaults to 1 for the last month

    this compares periods, so if the month has 31 days it will pull
    31 days back, even if that includes days in different months

    returns 4 values in a tuple
    1) start date of the month selected
    2) end date of the month selected
    3) start date of the period (same number of days) previous
    4) end date of the period (same number of days) previous
    """
    day_one = dt.date.today().replace(day=1)
    s_date_last = day_one - relativedelta(months=months_back)
    e_date_last = s_date_last + relativedelta(months=1) - relativedelta(days=1)
    s_date_prev = s_date_last - relativedelta(days=1) - (e_date_last - s_date_last)
    e_date_prev = s_date_last - relativedelta(days=1)
    return s_date_last, e_date_last, s_date_prev, e_date_prev


def _get_historical_weeks(weeks_back: int = 1) -> tuple:
    """
    takes in an int representing the number of week you want to go back
    defaults to 1 for the last week

    returns 4 values in a tuple
    1) start date of the week selected
    2) end date of the week selected
    3) start date of the period (same number of days) previous
    4) end date of the period (same number of days) previous
    """
    last_week_end = dt.date.today() - relativedelta(
        days=(weeks_back * dt.date.today().weekday()) + 2
    )
    last_week_start = last_week_end - relativedelta(days=6)
    prev_week_end = last_week_start - relativedelta(days=1)
    prev_week_start = prev_week_end - relativedelta(days=6)
    return last_week_start, last_week_end, prev_week_start, prev_week_end


class GSCReport:
    """One dimension report from GSC"""

    def __init__(
        self,
        site_name: Optional[str] = None,
        dimension: str = "page",
        date_range: str = "m",
        results_rows: int = 5,
        google_sheet_url: Optional[str] = None,
        print_out: bool = False,
    ):
        """
        Parameters:
        site_name: property name from GSC, can pass in None to declare it later:
            default: None
        dimension: SINGULAR GSC dimension, this will only compare one one dimension
            default: 'page'
        date_range: which periods you want to use month or week
            date_range options = ['m','w']
            default: 'm'
        results_rows: number of rows you want to output for comparison categories
            default: 5
        google_sheet_url: if you want to create a Google Sheet Report, pass in URL
            default: None
        print_out: do you want to print to console the results?
            default: False
        """
        self.set_site(site_name)
        self.set_dimension(dimension)
        self.results_rows = results_rows
        self.out_sheet = GoogleSheets(google_sheet_url)
        self.print_out = print_out

        # dates
        if date_range.lower() == "m":
            (
                self.last_period_start,
                self.last_period_end,
                self.prev_period_start,
                self.prev_period_end,
            ) = _get_historical_months(1)
            self.period_name = "Monthly"
        elif date_range.lower() == "w":
            (
                self.last_period_start,
                self.last_period_end,
                self.prev_period_start,
                self.prev_period_end,
            ) = _get_historical_weeks(1)
            self.period_name = "Weekly"
        else:
            raise TypeError(
                'Please select a correct date range. Either "M" for monthly or "W" for weekly'
            )

        """variables to be assigned while running"""

        # pd.DataFrames of GSC data
        self.last_period = None
        self.previous_period = None

        # an object of the CompareDF class
        self.compare_obj = None

        # pd.DataFrame from CompareDF class
        self.compare_df = None

        # GoogleSearchConsole object from googlewrapper
        self.gsc = None

    def set_site(self, site_name: str) -> None:
        """Set the current site name"""
        self.site_name = site_name

    def set_dimension(self, dimension: str) -> None:
        """Set which dimension this class will pull"""
        self.dim = dimension
        self.dim_proper = dimension.title()

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the response DF to have the dimension be the index"""
        # group by our dimension, and get sum of clicks and impressions
        temp = df.groupby(self.dim_proper).sum()[["Clicks", "Impressions"]].copy()
        # group by dimension, and provide mean of position -> assign this to Position column
        temp["Position"] = df.groupby(self.dim_proper).mean()["Position"]
        # calculate the CTR
        temp["CTR"] = temp["Clicks"] / temp["Impressions"]
        return temp

    def _url_subsections(self, subsection: str) -> None:
        """Extract a subsection of URL or Query containing subsection"""

        # find which sections (Page or Query) contain the subsection
        sub = self.compare_df.loc[
            self.compare_df.index.get_level_values(0).str.contains(subsection)
        ].copy()

        # declare which index level is melted Clicks, Impressions, Position
        # this is always the last index level
        column_index = len(self.compare_df.index.names) - 1

        # get the sum and mean columns to summarize
        ci = sub.loc[
            sub.index.get_level_values(column_index).isin(["Clicks", "Impressions"])
        ].copy()
        p = sub.loc[
            sub.index.get_level_values(column_index).isin(["Position", "CTR"])
        ].copy()
        pctr = p.groupby(p.index.get_level_values(column_index)).mean()
        ci = ci.groupby(ci.index.get_level_values(column_index)).sum()

        summary = ci.append(pctr)

        # add pct change column for comparison
        summary["pct"] = summary["change"] / summary["from"]

        if self.print_out:
            print(f"\n--{subsection}--\n")
            print(summary.round(2))

        # send to Google Sheets
        self._send(f"{subsection}'s Summary", summary.round(2))

    def _send(self, name: str, df: pd.DataFrame) -> None:
        """Create a tab in the current sheet, and fill it with df"""
        if self.out_sheet is not None:
            self.out_sheet.add_tab(name, df)

    def _pull_gsc_data(self):
        """
        calls GSC api for 2 periods (only one dimension of aggregation)
        assigns self.gsc to the GSC googlewrapper object if you need it later
        """
        # set up GSC object
        gsc = GoogleSearchConsole()
        gsc.set_sites([self.site_name])
        gsc.set_dimensions([self.dim])

        # get last periods data
        gsc.set_start_date(self.last_period_start)
        gsc.set_end_date(self.last_period_end)
        self.last_period = gsc.get_data()[self.site_name]

        # get previous periods data
        gsc.set_start_date(self.prev_period_start)
        gsc.set_end_date(self.prev_period_end)
        self.previous_period = gsc.get_data()[self.site_name]

        # assign gsc object to the class
        self.gsc = gsc

    def compare(self) -> None:
        """
        compares those values using the CompareDF class
        sends comparison df to Google Sheet
        """
        self._pull_gsc_data()

        # call the compare class to get what changed from the last period
        self.compare_obj = Compare(
            self._clean(self.previous_period), self._clean(self.last_period)
        )
        self.compare_obj.set_change_comparison(True)
        self.compare_obj.compare()

        # assign the df to the calss and calculate pct
        # change the index name to the dimension we used
        self.compare_df = self.compare_obj.change_detail
        self.compare_df["pct"] = self.compare_df["change"] / self.compare_df["from"]
        # self.compare_df.index.name = self.dim_proper

        # send to Google Sheet
        self._send("Comparison", self.compare_df)

    def highs_and_lows(
        self, percent_sort: bool = False, filter_zero_values: bool = True
    ) -> None:
        """
        Calculates the highest and lowest change values for a GSC data pull
        This can be done on a percent, or gross basis depending on parameters

        Outputs the biggest winners and biggest losers to separate Google Sheet Tabs

        Parameters:
        percent_sort: if you want to sort off percent change
            default is to sort off gross values

        filter_zero_values: if you want to remove from/to values that equal 0
            default is to remove these values

        takes the top pages/queries that improved/declined
        and prints these values to the console
        """
        for x in ["Clicks", "Impressions", "CTR", "Position"]:
            column_index = len(self.compare_df.index.names) - 1
            temp = self.compare_df.loc[
                self.compare_df.index.get_level_values(column_index) == x
            ].sort_values("change", ascending=False)
            if filter_zero_values or percent_sort:
                temp = temp.loc[temp["from"] > 0].copy()
                temp = temp.loc[temp["to"] > 0].copy()

            if percent_sort:
                temp = temp.sort_values("pct", ascending=False)

            # print to console
            if self.print_out:
                print(f"\n--{x}--\n")
                if x != "Position":
                    print(
                        f"Biggest Lossers: {temp.tail(self.results_rows)[::-1]}\n\nBiggest Winners: {temp.head(self.results_rows)}"
                    )
                else:
                    print(
                        f"Biggest Lossers: {temp.head(self.results_rows)}\n\nBiggest Winners: {temp.tail(self.results_rows)[::-1]}"
                    )

            # save to GoogleSheet
            if x != "Position":
                self._send(f"{x}'s Biggest Lossers", temp.tail(self.results_rows)[::-1])
                self._send(f"{x}'s Biggest Winners", temp.head(self.results_rows))
            else:
                self._send(f"{x}'s Biggest Lossers", temp.head(self.results_rows))
                self._send(f"{x}'s Biggest Winners", temp.tail(self.results_rows)[::-1])

    def check_subsections(self, subsection_list: list) -> None:
        """
        takes in a list of strings (sections of the page/query)
        and prints the stats for those groups
        """
        for sub in subsection_list:
            self._url_subsections(sub)

    def check_previous_top_sites(
        self, num_sites: int = 10, filter_zero_values: bool = True
    ) -> None:
        """
        Looks at the previous period's top pages/queries and see how they changed
        outputs the results to Google Sheet Tabs called 'Previous Top...'

        Parameters:
        num_sites: how many sites you want to check
            default to 10 sites

        filter_zero_values: if you want to remove from/to values that equal 0
            default is to remove these values

        checks the top pages/queries in the from column and sees how they changed
        prints the results for each metrics to the screen
        """
        for x in ["Clicks", "Impressions", "CTR", "Position"]:
            column_index = len(self.compare_df.index.names) - 1
            old_top = self.compare_df.loc[
                self.compare_df.index.get_level_values(column_index) == x
            ].sort_values("from", ascending=False)
            if filter_zero_values:
                old_top = old_top.loc[old_top["from"] > 0].copy()
                old_top = old_top.loc[old_top["to"] > 0].copy()

            old_top = old_top.round(2)
            if self.print_out:
                print(f"\n--{x}--\n")
                if x != "Position":
                    print(old_top.head(num_sites))
                else:
                    print(old_top.tail(num_sites)[::-1])

            if x != "Position":
                self._send(f"{x}'s Previous Top Positions", old_top.head(num_sites))
            else:
                self._send(
                    f"{x}'s Previous Top Positions", old_top.tail(num_sites)[::-1]
                )

    def from_list(self, sites_data: list, parent_folder=None):
        """
        Pull from multiple sites (in a list) and create a Google Drive folder

        Parameters
        sites_data: list of GSC property data
        create_sheet: if you want to create a new google sheet
            type: bool
        parent_folder: ID of parent folder (your new periodly folder will be stored in)
            type: str
        """
        folder_id = self.out_sheet.auth.drive.create_folder(
            f"{self.dim_proper} GSC {self.period_name} Reports - {self.last_period_start}",
            parent_folder,
        )

        # init the summary df
        summary = pd.DataFrame()

        # loop through all sites
        for site in sites_data:
            # create a new sheet in specific folder
            self.out_sheet.create_sheet(
                f"{site} {self.dim_proper} Report - {self.last_period_start}",
                folder_id=folder_id,
            )
            # assign class site to the current name
            self.site_name = site
            self.compare()
            self.highs_and_lows()
            # self.check_subsections()
            self.check_previous_top_sites()
            # add summary to summary df
            summary = summary.append(self.compare_obj.summary())

        # update summary
        self.out_sheet.create_sheet(
            f"{self.period_name} {self.dim_proper} Summary Report - {self.last_period_start}",
            folder_id=folder_id,
        )
        self._send("SUMMARY", summary)
        self.out_sheet.delete_tab("Sheet1")


def example():
    # YOUR SITE HERE
    site = "example.com"
    # YOUR GOOGLE SHEET LINK HERE
    google_sheet_link = ""

    # create the report object
    report = GSCReport(site, "page", google_sheet=google_sheet_link)
    report.compare()
    # get the report subsections and send them to Google Sheets
    report.highs_and_lows()
    report.check_subsections(["/blog"])
    report.check_previous_top_sites()
    # get rid of the unused first sheet
    report.out_sheet.delete_sheet("Sheet1")
    # return the report object (not necessary, but can be used to re-run or compare)
    return report


if __name__ == "__main__":
    my_monthly_report = example()
