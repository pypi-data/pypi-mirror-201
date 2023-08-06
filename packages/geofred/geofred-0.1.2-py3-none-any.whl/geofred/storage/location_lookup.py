import os
import pandas as pd
from pkg_resources import resource_stream

from geofred.utils import build_map

locations_fname = "location_lookup.csv"

# this_dir = os.path.dirname(os.path.realpath(__file__))
# locations_fpath = os.path.join(this_dir, locations_fname)
locations_fpath = resource_stream("geofred.storage", f"{locations_fname}")

DF_LOCATIONS = pd.read_csv(locations_fpath)


def build_county_map():
    return build_map(DF_LOCATIONS, ["zip", "county"])


def build_msa_map():
    return build_map(DF_LOCATIONS, ["zip", "msa"])


MSA_MAP = build_msa_map()
COUNTY_MAP = build_county_map()
