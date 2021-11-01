"""API Wrapper for Google Analytics"""

import datetime as dt
from typing import Optional, Any
import pandas as pd

from .connect import Connection


class GoogleAnalytics:
    """
    Google Analytics Wrapper Class
    REMEMBER your 'client_secret.json' file in your PATH

    Parameters
    view: string of Google Analytics view ID
    auth: googleapiclient.discovery.Resource object
            created from the Connection class by default
            no need to mess with this
    default_view: string "df" to have output formated as pd.DataFrame
                  if anything else, will be dictionary formated

    GA CONNECTION REFERENCE
    https://developers.google.com/analytics/
    devguides/reporting/core/v4/rest/v4/reports/batchGet
    """

    def __init__(self, view: str, default_view: str = "df") -> None:

        self.auth = Connection().ga()
        self.set_view(view)
        self.make_df = bool(default_view)

        # initialize filters to not be applied
        # we can add them in using the appropriate methods
        self._dim_filter: list[tuple[Any, Any, Any, Any, Any]] = []
        self._dim_filter_grouping = "OR"
        self._metric_filter: list[tuple[Any, Any, Any, Any]] = []
        self._metric_filter_grouping = "OR"

        # Assigned throughout the class
        self._metrics: list[str] = ["pageviews"]
        self._dims: list[str] = ["organic"]
        self._s_date: dt.date = dt.date.today() - dt.timedelta(days=8)
        self._e_date: dt.date = dt.date.today() - dt.timedelta(days=1)
        self.raw_data: dict[Any, Any] = {}

    def set_view(self, view_id: str) -> None:
        """
        Sets the active view to the parameter of view_id
        """
        self.view_id = view_id

    def set_metrics(self, metric_list: list[str]) -> None:
        """
        Parameters
        metric_list: which ga metrics we want to use, ensure they are named correct
          type: list of strings

        for naming help:
          https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/?
        """
        self._metrics = metric_list

    def set_dimensions(self, dimension_list: list[str]) -> None:
        """
        Parameters
        dimension_list: which ga dimensions we want to use,
            ensure they are named correct
          type: list of strings

        if you would like to pull multiple days worth of data,
        and would like to maintain the time aggregation,
        remember to include one of the following:
            year, month, week, day, yearMonth, date
        or whatever breakdown you would like

        for naming help:
            https://ga-dev-tools.appspot.com/dimensions-metrics-explorer/?
        """
        self._dims = dimension_list

    def set_dimension_filters(
        self, dimension_filters: list[tuple[Any, Any, Any, Any, Any]]
    ) -> None:
        """
        Parameters
        dimension_filters: all the dimension filters
          type: list of tupes
        tuple structure = (dimension name, 'not', operator, expression, caseSensitive)

        dimensionName: dimension to be filtered
          type: str
        not:
          type: bool
          default: False
        operator: how to match
          possible values: ["REGEXP","BEGINS_WITH","ENDS_WITH",
                              "PARTIAL","EXACT","NUMERIC_EQUAL",
                              "NUMERIC_GREATER_THAN",
                              "NUMBER_LESS_THAN","IN_LIST"]
          type: str
          default: REGEXP
        expression: only first considered, unless operator is "IN_LIST"
          type: list of strings
        caseSensitive: does case matter?
          type: bool
          default False

        for more details:
          https://developers.google.com/analytics/devguides/
          reporting/core/v4/rest/v4/reports/batchGet#DimensionFilterClause
        """
        if not isinstance(dimension_filters, list):
            raise TypeError(
                "Please make sure you call filter setters with a list of tuples"
            )
        self._dim_filter = dimension_filters

    def set_dimension_filter_group(self, enum: str) -> None:
        """
        By default the grouping for multiple filters is "OR",
        Using this method allows to change that to "AND"
        """
        self._dim_filter_grouping = enum

    def set_metric_filters(
        self, metric_filters: list[tuple[Any, Any, Any, Any]]
    ) -> None:
        """
        Parameters
        metric_filters: all the metric filters
          type: list of tuples
        tuple structure = (metric name, not, operator, comparisonValue)

        metricName: name of metric to filter
          type: str
        not: True = Values Excluded, False = Values Included
          type: bool
          default: False
        operator: how you want to compare
          possible values: ["EQUAL", "LESS_THAN",
                        "GREATER_THAN","IS_MISSION"]
          type: string
        comparisonValue: number to compare to
          type: float/int

        for more details:
          https://developers.google.com/analytics/devguides/
          reporting/core/v4/rest/v4/reports/batchGet#operator_1
        """
        if not isinstance(metric_filters, list):
            raise TypeError(
                "Please make sure you call filter setters with a list of tuples"
            )
        self._metric_filter = metric_filters

    def set_metric_filter_group(self, enum: str) -> None:
        """
        By default the grouping for multiple filters is "OR",
        Using this method allows to change that to "AND"
        """
        self._metric_filter_grouping = enum

    def set_start_date(self, start_date: dt.date) -> None:
        """
        Parameters

        start_date: will assign s_date variable
          type: datetime
        """
        self._s_date = start_date

    def set_end_date(self, end_date: dt.date) -> None:
        """
        Parameters

        end_date: will assign e_date variable
          type: datetime
        """
        self._e_date = end_date

    def build_request(
        self,
        size: int = 100000,
        page_token: Optional[str] = None,
        hide_totals: bool = True,
        pull: bool = True,
    ) -> Optional[dict[str, Any]]:
        """
        Parameters:

        Previously have assigned the following
         variables using their respective modules
        self._s_date: start date:
          type: datetime.date
        self._e_date: ending date:
          type: datetime.date
        self._metrics: ga metrics:
          type: list
        self._dims: ga dimensions:
          type: list

        optional (still previously assgined):
        self._dims_filter: ga filter:
          type: list of tuple

        Passed in Parameters:
        size: max number of rows to return
          type: int
          default: 100,000 (max allowed by GA)
        page_token: if you reached your max, pass this in
                     to use this as starting row
          type: str
          default: None (start at 0)
        hide_totals: if you want to see totals in the response json
          type: bool
          default: False
        pull: if after building the request json you want to call the API
          type: bool
          default: True (will request data from the GA API)

        """
        req_obj = {
            "reportRequests": [
                {
                    "viewId": str(self.view_id),
                    "dateRanges": [
                        {
                            "startDate": self._s_date.strftime("%Y-%m-%d"),
                            "endDate": self._e_date.strftime("%Y-%m-%d"),
                        }
                    ],
                    "metrics": [{"expression": f"ga:{x}"} for x in self._metrics],
                    "dimensions": [{"name": f"ga:{x}"} for x in self._dims],
                    "pageSize": size,
                    "pageToken": page_token,
                    "hideTotals": hide_totals,
                }
            ]
        }

        if self._dim_filter is not None:
            req_obj["reportRequests"][0]["dimensionFilterClauses"] = [
                {
                    "operator": self._dim_filter_grouping,
                    "filters": [
                        {
                            "dimensionName": f"ga:{x[0]}",
                            "not": f"{x[1]}",
                            "operator": f"{x[2]}",
                            "expressions": f"{x[3]}",
                            "caseSensitive": f"{x[4]}",
                        }
                        for x in self._dim_filter
                    ],
                }
            ]
        if self._metric_filter is not None:
            req_obj["reportRequests"][0]["metricFilterClauses"] = [
                {
                    "operator": self._metric_filter_grouping,
                    "filters": [
                        {
                            "metricName": f"ga:{x[0]}",
                            "not": f"{x[1]}",
                            "operator": f"{x[2]}",
                            "comparisonValue": f"{x[3]}",
                        }
                        for x in self._metric_filter
                    ],
                }
            ]

        if pull:
            ga_data: dict[str, Any] = self.pull(req_obj)
            return ga_data

        return req_obj

    def pull(self, request_body: dict[str, Any]) -> pd.DataFrame:
        """
        Parameters:
        request_body: structured request body for API call,
                       created by using self.build_request
          type: dict

        this function is often called right after
        `self.build_request()` being triggered by the
        pull=True parameter from the previous module

        returns the data in two options depending on how the
        class was initialized self.make_df is the variable
        that will change this return

        1) a created pd.DataFrame
        2) a raw response body (dictionary)
        """
        self.raw_data = self.auth.reports().batchGet(body=request_body).execute()
        if self.make_df:
            return self._create_df()

        return self.raw_data

    def _create_df(self) -> pd.DataFrame:
        """
        Loops through the Google Analytics batchGet()
        response json to create a pd.DataFrame

        Assigns variable types to columns
        """
        final_df = pd.DataFrame()
        for report_section in self.raw_data["reports"]:
            met = []
            cols = report_section.get("columnHeader")
            dims = cols["dimensions"]

            for header in cols["metricHeader"]["metricHeaderEntries"]:
                met.append(header.get("name"))

            row_data = report_section["data"].get("rows")
            metric_df = pd.DataFrame(
                [m["metrics"][0]["values"] for m in row_data], columns=met
            )

            # assign the variable types
            for col in cols["metricHeader"]["metricHeaderEntries"]:
                col_name = col.get("name")
                if col_name in metric_df.columns:
                    if col.get("type") in ["FLOAT", "PERCENT", "TIME", "CURRENCY"]:
                        metric_df[col_name] = metric_df[col_name].astype(float)
                    elif col.get("type") in ["INTEGER"]:
                        metric_df[col_name] = metric_df[col_name].astype(int)

            dim_df = pd.DataFrame([d["dimensions"] for d in row_data], columns=dims)
            # format dfs for simple merge
            metric_df.index.name = "idx"
            dim_df.index.name = "idx"
            dim_df = dim_df.merge(metric_df, on="idx")
            dim_df.columns = [column.replace("ga:", "") for column in dim_df.columns]
            final_df = final_df.append(dim_df)

        return final_df
