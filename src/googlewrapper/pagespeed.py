"""API Wrapper for Google Pagespeed Insights"""

from urllib.parse import urlparse
from datetime import date
from typing import Any, Optional

import requests
from pandas import DataFrame


class PageSpeed:
    """
    Pagespeed Wrapper class

    Authentication is through API key
    """

    def __init__(self, key: str) -> None:
        self._key = key
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
        self.set_category()
        self.date = date.today()

        # assigned through the class
        self.url: Optional[str] = None
        self.device: Optional[str] = None

    def set_url(self, url) -> None:
        """
        Assign & Validate URL
        """

        def url_validation(url):
            try:
                result = urlparse(url)
                return all([result.scheme, result.netloc, result.path])
            except ValueError:
                return False

        if url_validation(url):
            self.url = url
        else:
            raise ValueError(f"{url} is not a valid URL")

    def set_device(self, device: str) -> None:
        """
        Assign devices
        """
        device_list = ["DESKTOP", "MOBILE"]
        if device.upper() in device_list:
            self.device = device.upper()
        else:
            raise ValueError(
                f"{device} is not a valid device type."
                f" Try one of the following: {device_list}"
            )

    def set_category(self, category: str = "PERFORMANCE") -> None:
        """
        Assign category
        """
        category_list = ["ACCESSIBILITY", "BEST_PRACTICES", "PERFORMANCE", "PWA", "SEO"]
        if category.upper() in category_list:
            self.category = category.upper()
        else:
            raise ValueError(
                f"{category} is not a valid category type."
                f" Try on of the following: {category_list}"
            )

    def pull(self, output: str = "df") -> DataFrame:
        """
        Call the API endpoint
        Return Results
        """
        try:
            request_string = (
                f"category={self.category}"
                f"&url={self.url}"
                f"&strategy={self.device}"
                f"&key={self._key}"
            )
        except AttributeError as missing_variable:
            raise AttributeError from missing_variable
        if output == "df":
            return self._create_df(requests.get(self.base_url + request_string).json())

        return requests.get(self.base_url + request_string).json()

    def _create_df(self, results: dict[Any, Any]) -> DataFrame:
        """
        Creates a pd.DataFrame from API response
        Don't call directly. Called from the self.pull method
        """
        # Performance Score
        performance_score = results["lighthouseResult"]["categories"]["performance"][
            "score"
        ]
        # Largest Contenful Paint
        largest_contentful_paint = results["lighthouseResult"]["audits"][
            "largest-contentful-paint"
        ]["numericValue"]

        # First Input Delay
        first_input_delay = int(
            round(
                results["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"][
                    "distributions"
                ][2]["proportion"]
                * 1000,
                1,
            )
        )
        # CLS
        cumulative_layout_shift = results["lighthouseResult"]["audits"][
            "cumulative-layout-shift"
        ]["displayValue"]

        # Largest Contenful Paint Score
        crux_lcp = results["loadingExperience"]["metrics"][
            "LARGEST_CONTENTFUL_PAINT_MS"
        ]["category"]

        # First Input Delay Score
        crux_fid = results["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"][
            "category"
        ]

        # CLS Score
        crux_cls = results["loadingExperience"]["metrics"][
            "CUMULATIVE_LAYOUT_SHIFT_SCORE"
        ]["category"]

        # format as list for entry into pd.DF
        score_data = [
            self.url,
            self.device,
            self.date,
            performance_score,
            largest_contentful_paint,
            first_input_delay,
            cumulative_layout_shift,
            crux_lcp,
            crux_fid,
            crux_cls,
        ]
        cols = [
            "URL",
            "DEVICE",
            "DATE",
            "PERFORMANCE_SCORE",
            "LCP",
            "FID",
            "CLS",
            "LCP_SCORE",
            "FID_SCORE",
            "CLS_SCORE",
        ]
        return DataFrame([score_data], columns=cols)
