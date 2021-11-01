"""API Wrapper for Google Sheets"""

from typing import Optional, Any
from pandas import DataFrame, Series

from .connect import Connection


class GoogleSheets:
    """
    Google Sheets Wrapper Class
    REMEMBER your 'client_secret.json' file in your PATH

    Parameters
    url: string of Google Sheet URL
    auth: googleapiclient.discovery.Resource object
            created from the Connection class by default
            no need to mess with this

    Uses the pygsheets library
    https://pygsheets.readthedocs.io/en/stable/index.html
    """

    def __init__(self, url: Optional[str] = None):
        self.url = url
        self.auth = Connection().pygsheets()
        if self.url is not None:
            self.sheet_id = self.__get_id()
            self.workbook = self.auth.open_by_url(self.url)
            self.sheet = self.workbook.sheet1

    def create_sheet(
        self,
        sheet_title: str,
        folder_id: Optional[str] = None,
        template_id: Optional[str] = None,
    ):
        """
        create a new worksheet and set it to the active workbook
        """
        self.workbook = self.auth.create(
            sheet_title, folder=folder_id, template=template_id
        )
        self.sheet = self.workbook.sheet1
        return self.workbook.id
        # self.set_sheet('Sheet1')

    def delete_sheet(self, file_id: str):
        """
        delete a worksheet by file_id
        """
        self.auth.drive.delete(file_id)
        return file_id

    def create_folder(
        self, folder_name: str, parent_folder: Optional[str] = None
    ) -> str:
        """
        Create a folder in a specific location in your Drive
        If parent_folder is not supplied, folder will be create in Drive home
        """
        created_folder_id: str = self.auth.drive.create_folder(
            folder_name, parent_folder
        )
        return created_folder_id

    def __get_id(self) -> Optional[str]:
        """
        extracts the sheet id from the passed in URL
        """
        if self.url is not None:
            return self.url.split("d/")[1].split("/edit")[0]
        return None

    def set_tab(self, tab_name: str) -> None:
        """
        set the active tab to tab_name
        """
        self.sheet = self.workbook.worksheet("title", tab_name)

    # Spreadsheet/Tab Methods
    def get_df(self, start: str = "a1", index: int = 1, tailing: bool = False) -> DataFrame:
        """
        gets the contents of the sheet, and returns it as a pd DataFrame

        https://pygsheets.readthedocs.io/en/stable/worksheet.html#pygsheets.Worksheet.get_as_df
        """
        return self.sheet.get_as_df(
            start=start, index_column=index, include_tailing_empty=tailing
        )

    def save(
        self,
        data: DataFrame,
        start: str = "a1",
        index: bool = True,
        header: bool = True,
    ) -> None:
        """
        Saves a pandas DataFrame to the active sheet
        """
        if isinstance(data, DataFrame):
            self.sheet.set_dataframe(
                data, start, copy_index=index, copy_head=header, extend=True
            )
        elif isinstance(data, Series):
            self.sheet.set_dataframe(
                DataFrame(data), start, copy_index=index, copy_head=header, extend=True
            )
        else:
            raise TypeError("Please pass in a pd.DataFrame to save to Google Sheets")

    def clear(self, start: str = "a1", end: Optional[str] = None) -> None:
        """
        clears the contents of a worksheet

        both parameters are in 'a1' notation
        start: starting cell to clear contents
                defaults to 'a1'
        end: ending cell to clear contents (defaults to None)
                defaults to None (will clear entire worksheet)

        """
        self.sheet.clear(start, end)

    def row(self, row_number: int) -> list[Any]:
        """
        returns a list containing the row values

        accepts row_number that corresponds
        to the row in the active sheet
        """
        row_data: list[Any] = self.sheet.get_row(
            row_number, include_tailing_empty=False
        )
        return row_data

    def col(self, col_number: int) -> list[Any]:
        """
        returns a list containing the column values

        accepts col_number that corresponds
        to the col in the active sheet
            A = 1
            B = 2
            etc.
        """
        column_data: list[Any] = self.sheet.get_col(
            col_number, include_tailing_empty=False
        )
        return column_data

    # Entire Workbook Methods
    def add_tab(self, sheet_name: str, data: DataFrame = None) -> None:
        """
        add a tab named sheet_name to your workbook

        you can pass in a pandas dataframe and that will be
        inserted into starting cell a1
        """
        self.workbook.add_worksheet(sheet_name)
        self.set_tab(sheet_name)
        if data is not None:
            self.save(data)

    def delete_tab(self, sheet_name: str) -> None:
        """
        delete a tab named sheet_name from your workbook
        """
        self.workbook.del_worksheet(self.workbook.worksheet("title", sheet_name))

    def share(
        self,
        email_list: Optional[list[str]] = None,
        role: str = "reader",
        role_type: str = "user",
    ) -> None:
        """
        shares the active sheet with all the emails in the email_list

        assigns the permissions as declared by the role variable
        ['organizer', 'owner', 'writer', 'commenter', 'reader']
        default: reader

        role_type
        ['user', 'group', 'domain', 'anyone']
        default: user

        example on how to share with anyone
        self.share([],role='reader', type='anyone')
        """
        if email_list is None:
            self.workbook.share([], role, "anyone")
        else:
            for email in email_list:
                self.workbook.share(email, role, role_type)
