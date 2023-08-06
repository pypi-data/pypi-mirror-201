import json
import math

import pandas as pd

# extra 1 row to include the top chart row
MAX_DISPLAY_ROW_COUNT = 1001


def create_df_json_obj(df: pd.DataFrame) -> dict:
    """
    Create a json object based on the top MAX_DISPLAY_ROW_COUNT rows of the pandas.DataFrame
    param: df: a pandas DataFrame
    """
    data = []
    df = df.head(MAX_DISPLAY_ROW_COUNT)

    for _, row in df.iterrows():
        row_records = {}
        for column_index, value in row.to_dict().items():
            if isinstance(value, float) and math.isnan(value):
                value = None
            row_records[column_index] = value
        data.append(row_records)
    df_json = {"schema": _get_df_schema(df), "data": data}
    return df_json


def _get_df_schema(df: pd.DataFrame):
    # ToDo: return type based on sagemaker-data-insights algorithm?
    return [{"name": column, "type": str(df[column].dtype)} for column in df.columns]


def is_valid_df_json(df_json_obj: dict) -> bool:
    """
    Validate if the df_json has valid schema and data
    """

    data = df_json_obj["data"]
    schema = df_json_obj["schema"]

    if type(data) != list or type(schema) != list:
        return False

    if len(data) == 0 or len(schema) == 0:
        return False

    column_names_from_schema = [column["name"] for column in schema]
    return (
        True
        if all(len(row.keys()) == len(column_names_from_schema) for row in data)
        else False
    )
