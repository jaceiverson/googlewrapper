from attr import dataclass
import pytest
import datetime as dt

from googlewrapper import GoogleSearchConsole


@dataclass
class GSCTestData:
    connection = GoogleSearchConsole()


@pytest.fixture(scope="session")
def gsc():
    return GSCTestData()


@pytest.mark.incremental
class TestUserHandling:
    def test_connect(self, gsc):
        assert gsc.connection

    def test_site_pull(self, gsc):
        pass

    def test_filtered_site_pull(self, gsc):
        pass

    def test_default_params_pull(self, gsc):
        pass

    def test_default_dates(self, gsc):
        assert gsc.connection.dates() == (
            dt.date.today() - dt.timedelta(days=7),
            dt.date.today(),
        )

    def test_no_sites_pull(self, gsc):
        pass

    def test_setting_dimensions(self, gsc):
        pass

    def test_setting_metrics(self, gsc):
        pass

    def test_setting_filter(self, gsc):
        pass

    def test_ctr(self, gsc):
        pass
