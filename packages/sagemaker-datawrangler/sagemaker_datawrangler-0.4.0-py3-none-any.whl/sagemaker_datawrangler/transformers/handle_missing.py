import numpy as np
from pandas.api.types import is_numeric_dtype

from sagemaker_datawrangler.insights.insights_constants import (
    InsightsInfo,
    InsightsThresholds,
)

from .utils import get_mode, replace, replace_with_None


# recommended for both missing and disguised missing
def impute_mode(input_df, input_column, column_insights=None, warning_name=None):
    values_to_ignore = None
    missing_values = (
        column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES)
        if column_insights
        else None
    )
    if missing_values:
        values_to_ignore = set(
            column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES)
        )
    mode = get_mode(input_df, input_column, values_to_ignore)
    code = f"mode = '{mode}'\n"
    # disguised missing
    if missing_values:
        code += replace(missing_values, mode, input_column)
    # missing values
    else:
        code += (
            f"output_df['{input_column}']=output_df['{input_column}'].fillna(mode)\n"
        )
    return code


# recommended for numeric columns for missing values
def impute_median(input_df, input_column, column_insights=None, warning_name=None):
    return f"output_df['{input_column}']=output_df['{input_column}'].fillna(output_df['{input_column}'].median(skipna=True))"


# recommended for numeric columns for missing values
def impute_mean(input_df, input_column, column_insights=None, warning_name=None):
    return f"output_df['{input_column}']=output_df['{input_column}'].fillna(output_df['{input_column}'].mean())"


# recommend for both numeric and categorical for None and disguised missing
def impute_generic(input_df, input_column, column_insights=None, warning_name=None):
    col_data = input_df[input_column]
    if is_numeric_dtype(col_data):
        generic_value = 0
        code = f"generic_value = {generic_value}\n"
    else:
        generic_value = "Other"
        code = f"generic_value = '{generic_value}'\n"
    missing_values = (
        column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES)
        if column_insights
        else None
    )
    if missing_values:
        code += replace(missing_values, generic_value, input_column)
    else:
        code += f"output_df['{input_column}']=output_df['{input_column}'].fillna(generic_value)\n"
    return code


# Handle numeric_disguised_missing_value insight
def impute_nan(input_df, input_column, column_insights=None, warning_name=None):
    from_val, to_val = None, None
    if column_insights and column_insights.get(
        InsightsInfo.NUMERIC_DISGUISED_MISSING_VALUE
    ):
        from_val, to_val = (
            column_insights.get(InsightsInfo.NUMERIC_DISGUISED_MISSING_VALUE),
            None,
        )
    if column_insights and column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES):
        from_val, to_val = (
            column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES),
            None,
        )
    if from_val:
        if not isinstance(from_val, list):
            dtype = str(input_df[input_column].dtype)
            if "int" in dtype:
                from_val = int(from_val)
            if "float" in dtype:
                from_val = float(from_val)
            from_val = [from_val]
        code = replace_with_None(from_val, to_val, input_column)
        return code
    raise NotImplementedError


# drop rows with disguised missing and missing values
def drop_rows(input_df, input_column, column_insights=None, warning_name=None):
    # disguised missing values
    if column_insights and column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES):
        code = f"missing_values = {column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES)}\n"
        code += (
            f"output_df = output_df[~output_df['{input_column}'].isin(missing_values)]"
        )
        return code
    # non numeric values
    if column_insights and column_insights.get(InsightsInfo.NON_NUMERIC_VALUES):
        code = f"non_numeric_values = {column_insights.get(InsightsInfo.NON_NUMERIC_VALUES)}\n"
        code += f"output_df = output_df[~output_df['{input_column}'].isin(non_numeric_values)]"
        return code
    # missing values
    return f"output_df = output_df[output_df['{input_column}'].notnull()]"
