from googlewrapper import GoogleSearchConsole


def get_one_day(sites, d, dims, brand_dict):
    """
    Pulls one days worth of data for your GSC Property
    d: dt.datetime
    dims: list of GSC dimensions
    brand_dict: dictionary of branded terms
    """
    gsc = GoogleSearchConsole()
    gsc.set_date(d)
    gsc.set_dimensions(dims)
    gsc.set_sites(sites)
    gsc.set_branded(brand_dict)
    return gsc.get_data()
