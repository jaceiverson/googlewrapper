"""
Example of how to get custom CTR data for your property
"""
from googlewrapper import GoogleSearchConsole
import datetime as dt

# init object
gsc = GoogleSearchConsole()
# set our sites (here we want all under our credentials)
gsc.set_sites(gsc.all_sites())
# we want to get for the last 30 days
gsc.set_start_date(dt.date.today()-dt.timedelta(days=30))
gsc.set_end_date(dt.date.today())
# we will break down by query (allows for most accurate results)
gsc.set_dimensions(['query'])

# branded dictionary for more info see Docs
# https://github.com/jaceiverson/google-wrapper/blob/master/docs/Google%20Search%20Console.md#|%20Set%20Branded%20Queries

# YOUR BRANDED DICTIONARY HERE
branded_dict = {}
gsc.set_branded(branded_dict)

# call the GSC API
data = gsc.get_data()
# calculate custom CTRs
ctr = gsc.ctr()

# top 10 CTRs of all branded and non-branded together
top10_all = ctr['all']['CTR'].head(10)
# top 10 CTRs for branded only
top10_branded = ctr['branded']['CTR'].head(10)
# top 10 CTRs for non-branded only (most useful)
top10_non_branded = ctr['non-branded']["CTR"].head(10)
