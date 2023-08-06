import pandas as pd

from sagemaker_datawrangler.insights.insights_constants import Insights
from sagemaker_datawrangler.transformers.constants import OPERATORS, TRANSFORMER_NAMES


def is_valid_column_name(column_name: str, df: pd.DataFrame) -> bool:
    # Empty string indicates column was unselected
    return column_name == "" or column_name in df.columns


def is_valid_operator_id(operator_id: str) -> bool:
    valid_operators = {
        val for key, val in OPERATORS.__dict__.items() if not key.startswith("__")
    }
    return operator_id in valid_operators


def is_valid_transform_name(transform_name: str) -> bool:
    valid_transformer_names = {
        val
        for key, val in TRANSFORMER_NAMES.__dict__.items()
        if not key.startswith("__")
    }
    return transform_name in valid_transformer_names


def is_valid_warning_insight_id(warning_insight_id: str) -> bool:
    valid_warning_insight_id = {
        val for key, val in Insights.__dict__.items() if not key.startswith("__")
    }
    return warning_insight_id in valid_warning_insight_id


def is_valid_problem_type(problem_type: str) -> bool:
    return problem_type in ["Classification", "Regression"]


# ToDo: replace the hardcoded string to valid version patterns check
def is_valid_version(version) -> bool:
    return len(version) < 50
