### 0.2.11 (2022-9-2)

- BREAKING CHANGE: GoogleSheets.create_sheet() will now return the entire URL instead of the only the ID
- GoogleSheets.\_\_get_id() now uses the re library to extract id
- Updated GoogleSheets's tests to account for new return on create_sheet()
- Updated dependencies

### 0.2.10 (2022-5-18)

- Changed GSC for 1 site responses to return only a pd.DataFrame instead of a dictionary housing a DataFrame

### 0.2.9 (2022-2-15)

- New Feature: Reports Module
  - You can now run weekly/monthly reports using GSC/GA data
- Bug Fix: GoogleDocs.combine_content() now correctly joins highlighted/other formated text together

### 0.2.8 (2021-12-9)

- Bug Fix: Resolved GSC site_list issue with list like objects

### 0.2.7 (2021-11-12)

- Bug Fix: Resolved known authentiction issue (Issue #2)
- Added authentication for notebooks (colab, jupyter)

### 0.2.6 (2021-11-10)

- Added Google Docs (read only) wrapper

### 0.2.5 (2021-10-15)

- Clarified function names in GoogleSheets to more represent its action
- Methods that refer to tabs, are now properly labeled tab and not sheet

### 0.2.4 (2021-10-6)

- Bug Fix: GA.\_create_df() fixed column renaming issue

### 0.2.3 (2021-10-4)

- Tests added: Sheets, GSC (basic)
- Now formated with <a href=https://github.com/psf/black>black</a>
- Added type hints package wide
- Passing mypy, flake8 & pytest
- Expanded examples

### 0.2.2 (2021-09-07)

- Added feature to create brand new google sheet
- Changed relative import to remove module name for importing (from "googlewrapper.ga" to just "googlewrapper")

### 0.2.1 (2021-09-07)

- Fixed bug in sheets.py when deleting one tab

### 0.2.0 (2021-08-17)

- Clarified Doc Strings
- Ready for Beta testing

### 0.1.12 (2021-08-11)

- Removed blanket "except" in GSC class
- Added type hints through all classes

### 0.1.11 (2021-07-26)

- Added OR/AND filter options to GA class
- Fixed issue with how filters were applied to GA

### 0.1.10 (2021-06-24)

- Bug fix on branded queries strings resulting in empty tables

### 0.1.9 (2021-06-23)

- Added ability to find custom CTR with GSC data

### 0.1.8 (2021-06-10)

- Bug fix on GoogleSheets.col(). Now it returns values correctly

### 0.1.7 (2021-06-10)

- 0.1.6 did not actually work, now in 0.1.7 the dependencies are attached

### 0.1.6 (2021-06-10)

- Correctly added dependencies

### 0.1.5 (2021-06-08)

- Corrected how GSC classifies branded queries

### 0.1.4 (2021-06-08)

- Added basic functionality for GoogleSheets

### 0.1.3 (2021-06-07)

- Wrappers now will connect by default, simplifies the initializing of the classes

### 0.1.2 (2021-05-26)

- Cleaned up commenting and started with preliminary tests

### 0.1.0 (2021-05-26)

- BETA version
- Connect to various Google APIs
- First build
