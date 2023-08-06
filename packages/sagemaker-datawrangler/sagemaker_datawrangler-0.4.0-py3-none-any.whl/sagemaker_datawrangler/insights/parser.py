import json
import logging
import os
from pathlib import Path

import pandas as pd

from .utils import parse_int64_to_pyint


def parse_column_statistics(column_profiles, column_data: pd.Series):
    """
    Parse the raw column statistics data for frontend usage and compute stats based on pandas.Series.describe
    param: column_profiles: the raw column statistics
    """
    logical_data_type = column_profiles["logicalDataType"].upper()
    statistics = {
        **column_data.describe().to_dict(),
        "mode": column_data.mode(dropna=True).iat[0],
    }
    # JSON cannot parse np.int64 so need to convert to py int
    statistics = parse_int64_to_pyint(statistics)
    parsed_column_statistics = {
        "logicalDataType": logical_data_type,
        "validRatio": column_profiles["validRatio"],
        "invalidRatio": column_profiles["invalidRatio"],
        "missingRatio": column_profiles["missingRatio"],
        "totalCount": column_data.shape[0],
        "statistics": statistics,
    }
    if logical_data_type in ["CATEGORICAL", "BINARY", "TEXT"]:
        parsed_column_statistics["stats"] = {
            "distinctValues": len(column_profiles["columnProfile"]["data"]),
            "frequentElements": column_profiles["columnProfile"]["data"],
        }
    else:
        parsed_column_statistics["stats"] = column_profiles["columnProfile"]["data"]
    return parsed_column_statistics
