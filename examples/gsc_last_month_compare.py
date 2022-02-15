"""Create a report comparing 2 periods in GSC"""
from googlewrapper.reports import GSCReport

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
