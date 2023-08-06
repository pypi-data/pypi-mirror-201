import os
import logging
from typing import Union, List

import pandas as pd
import numpy as np
import fred

from geofred.utils import (
    search_with_filter,
    get_search_terms,
    get_locations_df,
    make_valid_key
)


def key(api_key): 
    fred.key(api_key)


def search(topics: Union[str, List[str]], **kwargs):
    """Return dataframe with relevant FRED series names"""
    search_terms = get_search_terms(topics)

    data_container = []
    for i, term in enumerate(search_terms):
        df_tmp = search_with_filter(term, **kwargs)
        logging.debug(f"found data with shape {df_tmp.shape}")
        data_container.append(df_tmp)

    if len(data_container) == 0:
        return pd.DataFrame()
    return pd.concat(data_container)


def data(series_df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """Input the DataFrame result of a 'search' call"""
    data_container = []
    ids = series_df["id"].values
    locations = series_df["location"].values
    topics = series_df["topic"].values
    aggregations = series_df["aggregation"].values
    for i, series_id in enumerate(ids):
        try:
            res = fred.observations(series_id, **kwargs)
            df_tmp = pd.DataFrame(res["observations"])
            logging.debug(f"{series_id}: found data with shape {df_tmp.shape}")

            df_tmp = df_tmp.drop(["realtime_start", "realtime_end"], axis=1)
            df_tmp["value"] = df_tmp["value"].apply(
                lambda x: np.nan if x == "." else x).str.replace(",", "").apply(pd.to_numeric)
            df_tmp["id"] = ids[i]
            df_tmp["location"] = locations[i]
            df_tmp["topic"] = topics[i]
            df_tmp["aggregation"] = aggregations[i]

            logging.debug(f"adding data to container.")
            data_container.append(df_tmp)
        except:
            logging.info(f"no data found for {series_id}")
    return pd.concat(data_container, axis=0, join="outer")


def locations(zips: Union[List[int], List[str]]) -> pd.DataFrame:
    """Return a dataframe of relevant location information. 

    :param zips: a pandas Series object of zipcodes. 
    """
    zips_ds = pd.Series(zips)
    zips = zips_ds.apply(make_valid_key).drop_duplicates().sort_values().values
    loc_df = get_locations_df()
    idxs = loc_df['zip'].isin(zips)
    return loc_df.loc[idxs, :].reset_index(drop=True)
