import os
import logging
import traceback

import pandas as pd

import fred


def do_search(topic: str, **kwargs) -> pd.DataFrame:
    """Search St. Louis Federal Reserve FRED API for relevant data series.

    Currently, using their API has several challenges for our use:
        0. pulling data relies on knowing their series ID
        1. it is not easy to search for series IDs by topic and aggregation level.
        2. it is not easy to match the resulting search IDs with a FedEx location.

    To solve this, we do the following processing on a raw FRED API search:
        - continue updating the offset as long as their internal return limit is reached
          this ensure we return all the available series IDs.
        - transform the resutling series dictionary into a pandas DataFrame for ease of use.
        - parse the FRED title into topic, location, and aggregation.

    :param topic: a string topic to search.
    :param freq: a FRED frequency e.g. Annual, Monthly, Quarterly.
    :param api_key: a valid FRED API key.
        For more information, see: https://fredaccount.stlouisfed.org/apikeys.
    """
    if "api_key" not in kwargs.keys():
        logging.info("No FRED API key included. Looking in local environment for key.")
        try:
            api_key = os.environ["FRED_API_KEY"]
        except KeyError:
            logging.error("ERROR: FRED_API_KEY not set.")
            logging.warning("To set key, run: \n    >>> fred.key('YOUR_API_KEY')")
            return pd.DataFrame()
    else:
        api_key = kwargs.pop("api_key")
        os.environ["FRED_API_KEY"] = api_key

    # TODO: avoid initiating this each time.
    api = fred.Fred(api_key=api_key)

    df = pd.DataFrame()
    offset = 0
    limit = 1000
    throws_error = False

    kwargs["search_text"] = topic
    if "freq" in kwargs.keys():
        kwargs["filter_variable"] = "frequency"
        kwargs["filter_value"] = kwargs.pop("freq")

    # the api limits to 1000 results by default.
    # if we hit this limit, we can include an offset
    # to retrieve more info.
    while True:
        # update offset if needed
        kwargs["offset"] = offset

        res = None
        try:
            logging.debug(f"doing search for {topic}.")
            res = api.series("search", **kwargs)
            logging.debug(f"got response from fred API.")

            series_data = res["seriess"]
            df_tmp = pd.DataFrame(series_data)
            if "title" in df_tmp.columns:
                logging.debug(f"found data with shape {df_tmp.shape}.")

                series_info = df_tmp["title"].apply(parse_fred_title)
                df_tmp["topic"] = series_info.apply(lambda x: x[0])
                df_tmp["location"] = series_info.apply(lambda x: x[1])
                df_tmp["aggregation"] = series_info.apply(lambda x: x[2])

                logging.debug(
                    f"parsed into updated dataframe with shape {df_tmp.shape}."
                )
                df = pd.concat([df, df_tmp])
        except Exception as e:
            logging.error(e, exc_info=True)
            throws_error = True

        if res is None or (len(res.get("seriess", [])) < limit or throws_error):
            break
        offset += limit
        logging.info(f"api response limit reached. incrementing offset to {offset}")
    return df


def search_with_filter(term: str, **kwargs) -> pd.DataFrame:
    df_search_results = do_search(term, **kwargs)

    # check if any data was returned
    logging.debug(f"found data with shape {df_search_results.shape}")
    if df_search_results.shape[0] == 0:
        return pd.DataFrame()

    # apply filters
    if "locations" in kwargs.keys():
        locations = kwargs.pop("locations")
        df_search_results = df_search_results.loc[
            df_search_results["location"].isin(locations), :
        ]
    if "sa" in kwargs.keys():
        sa = kwargs.pop("sa")
        logging.debug(f"looking for {sa} seasonal adjustment.")
        df_search_results = df_search_results.loc[
            df_search_results["seasonal_adjustment_short"] == sa, :
        ]
    if "agg" in kwargs.keys():
        agg = kwargs.pop("agg")
        logging.debug(f"looking for {agg} aggreagation level.")
        df_search_results = df_search_results.loc[
            df_search_results["aggregation"] == agg, :
        ]
    if "topic" in kwargs.keys():
        topic = kwargs.pop("topic")
        logging.debug(f"looking for {topic} specific topics.")
        df_search_results = df_search_results.loc[
            df_search_results["topic"] == topic, :
        ]
    return df_search_results.reset_index(drop=True)


def parse_fred_title(title):
    """
    parse the fred title for the following information:
        - series
        - location
        - aggregation type i.e. National, State, MSA, County
    INPUT
    :param title: str, a FRED title e.g. 'Average Hourly Earnings of All Employees, Total Private'
    OUTPUT
    :param topic: str, the concept of the series
    :param location: str, the location e.g. Maryland
    :param location_type: str, the aggregation type e.g. MSA or State
    """
    # import state lookup table here to avoid circular dependency
    from geofred.storage.state import STATE_MAP

    parse_token = " in "
    title_list = title.split(parse_token)

    # several cases to parse:
    # 1- 'blah topic in LOCATION'
    # 2- 'blah topic in industry'
    # 3- 'blah topic in industry in LOCATION'
    # 4- 'blah topic'
    if len(title_list) > 1:
        # check case 1 vs 2
        # three options:
        # 1- MSA or County
        # 2- State
        # 3- it's an industry
        topic, location = title_list[0].strip(), title_list[-1].strip()
        logging.debug(f"parsing title {title} into topic {topic} and location {location}")
        if "MSA" in location:
            agg_type = "MSA"
        elif "County" in location:
            agg_type = "County"
        elif STATE_MAP.get(location.strip(), "") != "":
            agg_type = "State"
        else:
            topic = title
            location = "The United States"
            agg_type = "National"
    else:
        # case 4
        topic, location, agg_type = title_list[0], "The United States", "National"
    return topic, location, agg_type


def make_valid_key(ele: int or str, zero_pad=True) -> str:
    """
    ensure zips are 5 digit strings

    INPUT
    :param zip: int
    OUTPUT - a zip string, padded with zeros as needed
    """
    pad_length = 5
    err_code = "ERROR"
    try:
        # coerce to string
        e = str(ele)
        if zero_pad: 
            num_zeros = pad_length - len(e)
            return "0" * num_zeros + e
        return e
    except:
        logging.error(f"unable to convert zip {zip} to string. returning {err_code}")
        return err_code


def build_map(df, cols: list, **kwargs) -> dict:
    """
    INPUT
    :param df: a pandas dataframe
    :param cols: a list of length two representing the columns that
                 will turn into the 'key' and 'value', respectively.
    OUTPUT - a lookup dictionary
    """
    assert len(cols) == 2
    assert isinstance(cols, list) or isinstance(cols, tuple)
    df_tmp = df.loc[:, cols].copy()

    result_dict = {}
    for _, row in df_tmp.iterrows():
        k = make_valid_key(row[cols[0]], **kwargs)
        v = row[cols[1]]
        result_dict[k] = v
    return result_dict


def get_locations_df():
    from geofred.storage.location_lookup import DF_LOCATIONS

    DF_LOCATIONS["zip"] = DF_LOCATIONS["zip"].apply(make_valid_key)
    return DF_LOCATIONS


def get_search_terms(series_name):
    terms = []
    for s in series_name:
        phrase = ""
        for i in s:
            if i.isalnum() or i == " ":
                phrase += i
        terms.append(phrase)
    logging.debug(f"looking for terms {terms}")
    return terms
