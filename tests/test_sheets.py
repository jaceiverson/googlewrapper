from attr import dataclass
import pytest
from pandas import DataFrame, Series

from googlewrapper import GoogleSheets


@dataclass
class SheetsTestData:
    s = GoogleSheets()
    sample_df = DataFrame([[1, 2, 3, 4]], columns=["A", "B", "C", "D"])
    sample_series = Series([1, 2, 3, 4], name="E")
    file_id = None
    folder_id = None
    my_url = None


@pytest.fixture(scope="session")
def sheet():
    return SheetsTestData()


@pytest.mark.incremental
class TestUserHandling:
    def test_login(self, sheet):
        assert sheet.s

    def test_folder_creation(self, sheet):
        sheet.folder_id = sheet.s.create_folder("PYTEST FOLDER TEST")
        assert sheet.folder_id

    def test_sheet_creation(self, sheet):
        sheet.file_id = sheet.s.create_sheet(
            "PYTEST CREATION TEST", folder_id=sheet.folder_id
        )
        sheet.my_url = f"https://docs.google.com/spreadsheets/d/{sheet.file_id}"
        assert sheet.file_id

    def test_init_with_url(self, sheet):
        s_url = GoogleSheets(sheet.my_url)
        assert s_url

    def test_create_new_tab(self, sheet):
        assert sheet.s.add_tab("NEW TAB") is None

    def test_delete_tab(self, sheet):
        assert sheet.s.delete_tab("Sheet1") is None

    def test_save_data_df(self, sheet):
        assert sheet.s.save(sheet.sample_df) is None

    def test_pull_data(self, sheet):
        pulled_data = sheet.s.get_df()
        assert all(sheet.sample_df.columns == pulled_data.columns)
        assert all(
            (pulled_data.values.astype(int) == sheet.sample_df.values.astype(int))[0]
        )

    def test_save_data_series(self, sheet):
        assert sheet.s.save(sheet.sample_series, "a4") is None

    def test_save_bad_data(self, sheet):
        with pytest.raises(TypeError):
            sheet.s.save("BAD DATA")

    def test_row(self, sheet):
        row = sheet.s.row(2)
        assert row == ["0", "1", "2", "3", "4"]

    def test_col(self, sheet):
        col = sheet.s.col(2)
        assert col == ["A", "1", "", "E", "1", "2", "3", "4"]

    def test_clear(self, sheet):
        assert sheet.s.clear() is None

    def test_save_data_new_tab(self, sheet):
        assert sheet.s.add_tab("NEW DATA TAB", sheet.sample_df) is None

    def test_share_globally(self, sheet):
        assert sheet.s.share() is None

    def test_share_user(self, sheet):
        assert sheet.s.share(["iverson.jace@gmail.com"], "reader") is None

    def test_deletion(self, sheet):
        deleted_id = sheet.s.delete_sheet(sheet.file_id)
        assert deleted_id == sheet.file_id
        deleted_folder_id = sheet.s.auth.drive.delete(sheet.folder_id)
        assert deleted_folder_id is None
