"""API Wrapper for Google Search Console"""

import datetime as dt
import warnings
from typing import Optional, Any
import pandas as pd
from numpy import nan

# nan is used in the "_check_branded" method
# probably can be removed, we just need to check
# if a list is empty, I'm sure there is a better way

from googlewrapper.connect import Connection


class GoogleSearchConsole:
    """
    Google Search Console Wrapper Class
    REMEMBER your 'client_secret.json' file in your PATH

    Parameters
    auth: googleapiclient.discovery.Resource object
            created from the Connection class by default
            no need to mess with this as long as your
            'client_secret.json' is in PATH
    """

    def __init__(self):

        # Google API Resourse Object created from
        # Connection class in .connect module
        self.auth = Connection().gsc()

        # default values for dimensions and date values
        # start date is 7 days ago
        # end date is today
        self._dims = ["page", "date"]
        self._s_date = dt.date.today() - dt.timedelta(days=7)
        self._e_date = dt.date.today()

        # attributes Assigned throughout the class

        # assigned using .set_sites()
        self._site_list: list[str] = self.all_sites()
        # assigned using .set_branded()
        self._branded_dict: dict[str, list[str]] = {}
        # assigned using .set_filters()
        self._filter: Optional[list[dict[str, str]]] = None
        # assigned in .get_data()
        self._current_site: str = ""
        self.output: Optional[pd.DataFrame] = None
        # assigned in .ctr()
        self.my_ctr: Optional[pd.DataFrame] = None

    def __str__(self) -> str:
        if len(self._site_list) > 1:
            return f"Custom GSC Wrapper for {len(self._site_list)} sites"
        if len(self._site_list) == 1:
            return f"Custom GSC Wrapper for {self._site_list[0]}"
        return "Custom GSC Wrapper"

    def __repr__(self) -> str:
        return f"<gsc-wrapper-object reference {self.auth}>"

    def dates(self) -> tuple[dt.date, dt.date]:
        """
        returns your current start and end dates in a tuple
        (start_date,end_date)
        """
        return self._s_date, self._e_date

    def set_sites(self, site_list: list[str]) -> None:
        """
        Assigns the self._site_list attribute. This controls what sites
        will get pulled when you call self.get_data()

        By default self._site_list is set to all verified sites you
        have access to. This is accessed using self._all_sites()

        :Params:
        site_list: list of sites (url strings) we want to pull from GSC API
            type: list
        """
        self._site_list = site_list

    def set_dimensions(self, dimensions: list[str]) -> None:
        """
        Assigns the self_.dims attribute. This is the list of dimensions
        that your data will be aggregated on when pulled using
        self.get_data().
        These dimensions will turn into columns in the DataFrame once complete.

        By default self._dims is set to ['page','date']

        :Params:
        d: what we want to break it down by
            type: list
            options: ['page','date','query', 'device','country']
        """
        self._dims = dimensions

    def set_filters(self, filter_object: list[dict[str, str]]) -> None:
        """
        Assigns the self._filter attribute. These filters are applied
        when calling self.get_data()

                example_filter = {
                        "dimension": string,
                        "operator": string,
                        "expression": string
                        }

        At this time the GSC api, only allows for dimension based filters

        If you would like a metric based filter, first pull all the data,
        then filter using pandas filtering/querying abilities

        :Params:
        filters_list: list of filters formated as GSC requires
        """
        self._filter = filter_object

    def set_date(self, date: dt.date) -> None:
        """
        Assigns the self._s_date and self._e_date attributes to the
        same date. This is used when you want only one date
        when pulling data using self.get_data()

        :Params:
        date: assigns the start and end date as the same day
            type: dt.datetime or dt.date
        """
        self._s_date = date
        self._e_date = date

    def set_start_date(self, start_date: dt.date) -> None:
        """
        Assign the self._s_date attribute. This is the first date
        (inclusive) of data that will be pulled when calling self.get_data()

        Defaults to 7 days from dt.date.today()

        :Params:
        start_date: the starting point (inclusive)
                        for the API pull
            type: dt.datetime or dt.date
        """
        self._s_date = start_date

    def set_end_date(self, end_date: dt.date) -> None:
        """
        Assign the self._e_date attribute. This is the last date
        (inclusive) of data that will be pulled when calling self.get_data()

        Defaults to dt.date.today()

        :Params:
        end_date: the ending point (inclusive)
                    for the API pull
            type: dt.datetime or dt.date
        """
        self._e_date = end_date

    def set_branded(self, branded_dictionary: dict[str, list[str]]) -> None:
        """
        Assigns the self._branded_dict attribute.
        When 'query' is one of the dimensions in self._dims,
        these terms will set the 'Branded' column in the
        final DataFrame output to True.

        This is not required and is None by default.
        This method and attribue have no effect if 'query' is not included in self._dims

        :Params:
        branded_dictionary: branded terms
            type: dictionary
            keys: GSC url properties
            values: list of branded strings
        """
        self._branded_dict = branded_dictionary

    def all_sites(self, site_filters: Optional[list[str]] = None) -> list[str]:
        """
        returns a list of all verfied sites that you have in GSC.

        It will give you all properties by default, but can be
        filtered using the site_filters parameter.

        :Example:
            site_filters = ['example','test']
        This would only return properties that contain the word 'example' or 'test'

        :Params:
        site_filters: (optional) strings to include if found in property urls
            type: list
        """
        site_list = self.auth.sites().list().execute()
        clean_list: list[str] = [
            s["siteUrl"]
            for s in site_list["siteEntry"]
            if s["permissionLevel"] != "siteUnverifiedUser"
            and s["siteUrl"][:4] == "http"
        ]
        if isinstance(site_filters, list):
            return [
                site
                for site in clean_list
                if any(word in site for word in site_filters)
            ]
        return clean_list

    def _build_request(
        self, agg_type: str = "auto", limit: int = 25000, start_row: int = 0
    ) -> dict[Any, Any]:
        """
        Creates a dictionary object that will be used in the API request.
        This dicionary object contains specific attributes necessary for
        the request per the search console API. These attributes include:
            - "startDate"
            - "endDate"
            - "dimensions"
            - "aggregationType"
            - "rowLimit"
            - "startRow"
            - "dimensionFilterGroups"

        All of these variables need to be assigned before this method gets called.

        After creation, this method sends the requests dictionary to
        the self._execute_request() method

        NOTE: This method is only called from the
        self.get_data() method and should not be called directly.

        See the site below for more details:
        https://developers.google.com/webmaster-tools/
        search-console-api-original/v3/searchanalytics/query

        :Params:
        agg_type: (optional) auto is fine can be byPage or byProperty
            defaults "auto"
        limit: (optional) number of rows to return
            defaults 25000
        start_row: (optional) where to start, if need more than 25,000
            defaults 0
        """

        request_data = {
            "startDate": self._s_date.strftime("%Y-%m-%d"),
            "endDate": self._e_date.strftime("%Y-%m-%d"),
            "dimensions": self._dims,
            "aggregationType": agg_type,
            "rowLimit": limit,
            "startRow": start_row,
            "dimensionFilterGroups": [{"filters": self._filter}],
        }

        return self._execute_request(request_data)

    def _execute_request(self, request: dict[Any, Any]) -> dict[Any, Any]:
        """
        Executes a searchAnalytics.query request based on the
        dictionary created in self._build_request()

        This method should not be called directly.

        Returns an dictionary of GSC response rows.

        :Params:
        request: dictionary created from the self._build_request() method
            type: dict
        """
        gsc_query_result: dict[Any, Any] = (
            self.auth.searchanalytics()
            .query(siteUrl=self._current_site, body=request)
            .execute()
        )

        return gsc_query_result

    def clean_resp(self, data: dict[Any, Any]) -> pd.DataFrame:
        """
        Takes raw response, and cleans the data into a pd.Dataframe

        Returns a pd.DataFrame
            columns: self._dims
            rows: GSC data from API request

        :Params:
        data: response dictionary from self._execute_request()
            type: dictionary
        """
        raw_df = pd.DataFrame(data["rows"])
        raw_df.index.name = "idx"
        keys = raw_df["keys"].apply(pd.Series)
        keys.columns = self._dims
        raw_df = raw_df.merge(keys, how="left", on="idx")
        raw_df.drop(columns="keys", inplace=True)
        raw_df.columns = raw_df.columns.str.capitalize()

        # branded check
        if isinstance(self._branded_dict, dict) and "Query" in raw_df.columns:
            raw_df["Branded"] = self._check_branded(raw_df["Query"])

        # convert to datetime
        if "Date" in raw_df.columns:
            raw_df["Date"] = pd.to_datetime(raw_df["Date"])

        raw_df[["Clicks", "Impressions"]] = raw_df[["Clicks", "Impressions"]].astype(
            int
        )

        return raw_df

    def _check_branded(self, query_list: pd.Series) -> pd.Series:
        """
        Takes in a pd.Series of queries (from self.clean_resp())
        and returns a pd.Series of booleans on if the
        query contains any word from the self._branded_dict

        :Params:
        query_list: 'queries' from GSC API request
            type: pd.Series
        """
        try:
            branded_list: list[str] = self._branded_dict[self._current_site]
        except KeyError:
            return False
        if branded_list in [nan, [], [""]]:
            return False
        return pd.Series(query_list).str.contains("|".join(branded_list), na=False)

    def get_data(self) -> dict[Any, Any]:
        """
        Main method to access data.
        Loops through the self._site_list
        calls self._build_request() -> self._execute_request()

        cleans the response using self.clean_resp()

        Creates a dictionary named 'gsc_analytics_data'
            keys: GSC property name
            values: cleaned pd.DataFrame of GSC data

        Once all properties have been accounted for the attribute
        'self.output' is assigned the value of 'gsc_analytics_data'

        this final dictionary of 'gsc_analytics_data' is returned.
        """
        # check to make sure self._site_list is declared
        if not self._site_list:
            raise AttributeError(
                "Please declare self._site_list"
                " using the .set_sites() method prior to running .get_data"
            )
        gsc_analytics_data = {}
        for site_name in self._site_list:
            self._current_site = site_name
            start = 0
            row_limit = 25000
            temp_df = pd.DataFrame()
            # loop through the api grabbing the maximum rows possible
            while True:
                # get the data from the api
                response = self._build_request(limit=row_limit, start_row=start)
                # if rows is in response.keys, we have data from the API
                if "rows" in response.keys():
                    cleaned_df = self.clean_resp(response)
                    temp_df = temp_df.append(cleaned_df)
                    start += row_limit
                # if not, we have pulled the max rows, we need to break/go to next property
                else:
                    break
            # assign the temp_df (current_site_df) to our final dict
            gsc_analytics_data[site_name] = temp_df

        # declare the data as output and save to class
        # this could be large, could have memory issues, need to
        # look into this
        self.output = gsc_analytics_data

        return gsc_analytics_data

    def ctr(self) -> dict[str, pd.DataFrame]:
        """
        Used after we have called .get_data()
        Calulcates a custom click curve for the given data that you have pulled

        Returns
        a dictionary with the following keys:
            - "all"
                a general CTR given all the data
            - "branded"
                a CTR for only branded queries
            - "non-branded"
                a CTR for only non-branded queries

        There are a few things that throw off the custom CTR calculations:

        1) If "query" is included as a dimension when we pulled the data
            if not included, we will see weird numbers
            make sure that query is included in dimensions
            use .set_dimensions()

        2) If there are branded queries
            We tend to see branded queries experience a higher CTR,
            and will thus inflate your numbers if we don't separate them
            declare branded queries using .set_branded()
        """
        if not self.output:
            raise AttributeError("Please run .get_data() prior to running .ctr()")

        if "query" not in self._dims:
            warnings.warn(
                '"query" is not an active dimension in your data.'
                " CTR calulcations are heavily influcenced by queries."
                ' It is reccomented to use the "query" dimension to ensure accurate CTR numbers.'
            )

        if not self._branded_dict:
            warnings.warn(
                "You have not declared any branded queries using .set_branded(dict)."
                " CTR calulcations are heavily influcenced by branded queries."
                " It is reccomented to assign brand words to ensure accurate CTR numbers."
            )

        # declare function to group by position and get CTR
        def calculate_ctr(gsc_df: pd.DataFrame, col: str) -> pd.DataFrame:
            """
            this groups by position and gives us our CTR

            df: type: pd.DataFrame
                data from the .get_data() formated as a pd.DataFrame
                this will group all sites in self._site_list together
            col: type: str
                is the string name of the column to groupby
                normally this should be 'Pos'
                as declared in .ctr() scope
            """
            ctr = gsc_df.groupby(col).sum()
            ctr["CTR"] = ctr["Clicks"] / ctr["Impressions"]

            if self._branded_dict:
                return ctr.drop(columns="Branded")

            return ctr

        # create the dataframe from response dictionary - .get_data() response
        response_df = pd.DataFrame()
        for site_name in self.output:
            response_df = response_df.append(self.output[site_name])
        # create the rounded position column
        response_df["Pos"] = response_df["Position"].round(0)

        # we only want to consider those queries in the top 100 positions
        # also, we only want Clicks, Impressions, and Pos, the rest doesn't matter
        if self._branded_dict:
            response_df = response_df.loc[response_df["Pos"] <= 100][
                ["Clicks", "Impressions", "Pos", "Branded"]
            ].copy()
        else:
            response_df = response_df.loc[response_df["Pos"] <= 100][
                ["Clicks", "Impressions", "Pos"]
            ].copy()

        # create the first dictionary object including all data
        ctr_data = {"all": calculate_ctr(response_df, "Pos")}

        # if Branded is in the columns we will separate the click curves into
        # Branded vs Non-Branded and return both as well
        if self._branded_dict:
            # use that function to get our custom CTR
            ctr_b = calculate_ctr(
                response_df.loc[response_df["Branded"] is True].copy(), "Pos"
            )
            ctr_nb = calculate_ctr(
                response_df.loc[response_df["Branded"] is False].copy(), "Pos"
            )

            ctr_data["branded"] = ctr_b
            ctr_data["non-branded"] = ctr_nb

        self.my_ctr = ctr_data

        return ctr_data
