"""API Wrapper for Google Big Query"""

from datetime import date
from typing import Optional
from google.cloud import bigquery
import pandas as pd

from .connect import Connection


class GoogleBigQuery:
    """
    Google Big Query Wrapper Class
    REMEMBER your 'gba-sa.json' file in your PATH
    This is different from the 'client_secret.json'

    Parameters
    auth_file_path: if your GBQ Service Account .json file
        is not in your path, you need to pass in the path here
    """

    def __init__(self, auth_file_path: str = "gbq-sa.json") -> None:
        self.auth = Connection().gbq(auth_file_path)
        self._client = bigquery.Client(credentials=self.auth)
        self._project: str = self.auth.project_id
        self._dataset: Optional[str] = None
        self._table: Optional[str] = None

    def set_dataset(self, dataset_name: str) -> None:
        """
        Assigns dataset_name to the active
        GBQ dataset name -> self._dataset
        """
        self._dataset = dataset_name

    def set_table(self, table_name: str) -> None:
        """
        Assigns table_name to the active
        GBQ table name -> self._table
        """
        self._table = table_name

    def full_table_name(self) -> str:
        """
        Combines self._dataset and self._table
        this becomes the full table name in GBQ

        Returns this combination as a string
        """
        return f"{self._dataset}.{self._table}"

    def list_datasets(self) -> list[str]:
        """
        returns a list of all dataset ids/names in the authorized client
        """
        return [x.dataset_id for x in list(self._client.list_datasets())]

    def send(
        self,
        data: pd.DataFrame,
        chunk_size: int = 10000,
        behavior: str = "append",
        progress_bar: bool = False,
    ) -> None:
        """
        sends the data (df parameter) into the
        active GBQ table (self._table) & dataset (self._dataset)

        Declare self._table and self._dataset prior to running
        this method

        :Params:
        df: data to be inserted into GBQ
            type: pd.DataFrame
        chunk_size: the size (rows) we will break the tables into to insert
            type: int
            default: 10,000 rows
        behavior: what to do if tables exists
            __OPTIONS__
            append: (default behavior) add to bottom of table
            fail: fail, no import happens
            replace: drop the table, insert current df

        progress_bar: do you want to see a progress bar in terminal
            type: bool
            default: False (no progress bar)
        """
        try:
            data.to_gbq(
                destination_table=f"{self._dataset}.{self._table}",
                project_id=self._project,
                chunksize=chunk_size,
                if_exists=behavior,
                progress_bar=progress_bar,
            )
        except AttributeError as project_name_missing:
            raise AttributeError from project_name_missing

    def read(self, query_string: str) -> pd.DataFrame:
        """
        Read from GBQ using a query string

        Returns a pd.DataFrame
        """
        queried_df = pd.read_gbq(
            query=query_string, project_id=self._project, progress_bar_type="None"
        )
        return queried_df

    def delete_day(self, date_to_delete: date, str_return: bool = False):
        """
        deletes the passed in day from the
        pre-determined table in GBQ
        """
        query_string = f"""
        DELETE
        FROM `{self._project}.{self._dataset}.{self._table}`
        WHERE
        EXTRACT(Year FROM `Date`) = {date_to_delete.year}
        AND
        EXTRACT(Month FROM `Date`) = {date_to_delete.month}
        AND
        EXTRACT(Day FROM `Date`) = {date_to_delete.day}
        """

        if str_return:
            return query_string

        return self._client.query(query_string)
