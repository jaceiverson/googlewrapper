"""Example of a GA & GSC Weekly Report"""

import datetime as dt
from googlewrapper.reports import WeeklyReport

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
