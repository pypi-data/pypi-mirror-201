import numpy as np
import pandas as pd

from sagemaker_datawrangler.insights.insights_constants import (
    MAX_EXAMPLES_TO_DISPLAY,
    InsightsThresholds,
)
from sagemaker_datawrangler.transformers.constants import (
    OPERATORS,
    ROW_BASED_TRANSFORMERS,
)

from .feature_column_insights_schema import FEATURE_COLUMN_INSIGHTS_INFO
from .insights_constants import Insights
from .target_column_insights_schema import TARGET_COLUMN_INSIGHTS_INFO

INSIGHTS_INFO_MAP = {**FEATURE_COLUMN_INSIGHTS_INFO, **TARGET_COLUMN_INSIGHTS_INFO}


def get_transforms_for_missing_insights(
    column_stats, missing_ratio=0, insight=Insights.HIGH_MISSING_RATIO
):
    recommended_transforms = INSIGHTS_INFO_MAP.get(insight)["operators"]
    data_type = column_stats.get("logicalDataType")
    data_type = data_type.lower() if data_type else None
    modified_recommended = []
    for transform in recommended_transforms:
        operator_id = transform["operator_id"]
        if operator_id == OPERATORS.DROP_COLUMN:
            transform["is_recommended"] = False
            if missing_ratio > InsightsThresholds.HIGH_MISSING_RATIO:
                transform["is_recommended"] = True
            modified_recommended.append(transform)
        elif operator_id in {OPERATORS.IMPUTE_MEAN, OPERATORS.IMPUTE_MEDIAN}:
            if data_type == "numeric":
                modified_recommended.append(transform)
            else:
                continue
        else:
            modified_recommended.append(transform)
    return modified_recommended


def is_table_level_transform(
    transform_name: str,
    previous_df: pd.DataFrame = None,
    updated_df: pd.DataFrame = None,
):
    """
    Returns True if it's a row based transform or df length is updated
    Args:
        transform_name: str, transformer name
        previous_df: pd.DataFrame, df from the previous state
        updated_df: pd.DataFrame, updated df after applying transform
    """

    # TODO: Need to add to row_based_transformers to the const, replace with better mechansim to automatically
    # detect if we can enable column granularity
    return (transform_name in ROW_BASED_TRANSFORMERS) or (
        len(previous_df) != len(updated_df)
    )


def get_column_highlights(column_name: str, column_data: pd.Series, column_insights):
    column_highlights = {}
    for insight in column_insights:
        warning = insight["warnings"]
        insight_id, insight_info = warning.get("insight_id"), warning.get("info")
        insight_info_key = INSIGHTS_INFO_MAP.get(insight_id).get("info_key")
        if insight_info and insight_info_key:
            column_highlights[insight_id] = insight_info[insight_info_key]
    return column_highlights


def parse_int64_to_pyint(data):
    for key, value in data.items():
        if type(value) == np.int64:
            data[key] = int(value)
    return data


def parse_insight_id(insight_key):
    insight_id_prefix = "sagemaker.data_quality."

    # ToDo: integrated with https://tiny.amazon.com/sgqcoejl/githawssageblob35a6srcsage
    if insight_key in [
        "Regression many non-numeric values",
        "Regression non-numeric values",
    ]:
        return insight_id_prefix + "non_numeric_values"
    elif insight_key in ["Many duplicate rows", "Duplicate rows"]:
        return insight_id_prefix + "duplicate_rows"
    else:
        return insight_id_prefix + insight_key.replace(" ", "_").lower()


def set_examples(example_str_prefix, example_values):
    if not example_str_prefix or not example_values:
        return None
    example_values = (
        [example_values] if not isinstance(example_values, list) else example_values
    )
    count_extra = len(example_values) - MAX_EXAMPLES_TO_DISPLAY
    example_values = example_values[:MAX_EXAMPLES_TO_DISPLAY]
    example_values = [f'"{str(val)}"' for val in example_values]
    example_str_prefix += ", ".join(map(str, example_values))
    if count_extra > 0:
        example_str_prefix += f" and {count_extra} more"
    return example_str_prefix
