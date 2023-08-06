import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype
from scipy import stats

from sagemaker_datawrangler.insights.data_quality_insights import INSIGHTS_INFO_MAP
from sagemaker_datawrangler.insights.insights_constants import (
    Insights,
    InsightsInfo,
    InsightsThresholds,
)
from sagemaker_datawrangler.insights.target_column_insights_schema import (
    TARGET_COLUMN_INSIGHTS_INFO,
)
from sagemaker_datawrangler.logging.logging import get_metrics_logger
from sagemaker_datawrangler.transformers.constants import OPERATORS
from sagemaker_datawrangler.transformers.utils import (
    get_mode,
    get_rare_categories,
    parse_and_retain_data_type,
    replace,
)

from .handle_missing import (
    drop_rows,
    impute_generic,
    impute_mean,
    impute_median,
    impute_mode,
    impute_nan,
)

metrics_logger = get_metrics_logger()


def get_impute_value(input_df, input_column, values_to_ignore=None):
    impute_value = None
    top_frequent = input_df[input_column].value_counts().index.tolist()
    for val in top_frequent:
        if values_to_ignore == None or val not in values_to_ignore:
            impute_value = val
            break
    return impute_value


def replace(from_values, to_value, input_col):
    code, regex = "", False
    to_value = f"'{to_value}'" if isinstance(to_value, str) else to_value
    for value in from_values:
        # replace empty string with regex
        if value == "":
            value = r"^\s*$"
            regex = True
        value = f"'{value}'" if isinstance(value, str) else value
        code += f"output_df['{input_col}']=output_df['{input_col}'].replace({value}, {to_value}, regex={regex})\n"
    return code


def _impute_numeric(input_df, input_column, column_insights=None, warning_name=None):
    # Impute numeric for common Missing types
    if column_insights and column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES):
        missing_values = column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES)
        filtered_df = input_df[~input_df[input_column].isin(missing_values)]
        median = filtered_df[input_column].median()
        code = f"median = {median}\n"
        code += replace(missing_values, median, input_column)
        return code
    return f"output_df['{input_column}']=output_df['{input_column}'].fillna(output_df['{input_column}'].median())"


def _impute_categorical(
    input_df, input_column, column_insights=None, warning_name=None
):
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
    impute_val = get_impute_value(input_df, input_column, values_to_ignore)
    code = f"impute_value = '{impute_val}'\n"
    code += f"output_df['{input_column}']=output_df['{input_column}'].fillna(impute_value)\n"
    if missing_values:
        code += replace(missing_values, impute_val, input_column)
    return code


def _drop_missing(input_df, input_column, column_insights=None, warning_name=None):
    if column_insights and column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES):
        code = f"missing_values = {column_insights.get(InsightsInfo.DISGUISED_MISSING_VALUES)}\n"
        code += (
            f"output_df = output_df[~output_df['{input_column}'].isin(missing_values)]"
        )
        return code
    if column_insights and column_insights.get(InsightsInfo.NON_NUMERIC_VALUES):
        code = f"non_numeric_values = {column_insights.get(InsightsInfo.NON_NUMERIC_VALUES)}\n"
        code += f"output_df = output_df[~output_df['{input_column}'].isin(non_numeric_values)]"
        return code
    return f"output_df = output_df[output_df['{input_column}'].notnull()]"


def _drop_outliers_with_robust_std(
    input_df, input_column, column_insights=None, warning_name=None
):
    """A method to exclude numeric outliers that depends on the data being normally distributed."""
    return f"output_df = output_df[(np.abs(stats.zscore(output_df['{input_column}'])) < 3)]"


# TODO: This will need to be wired into the transformer to code mapping in a follow up PR.
def _drop_outliers_with_quantile(
    input_df, input_column, column_insights=None, warning_name=None, quantile=0.99
):
    """A method to exclude numeric outliers that doesn't depend on the data being normally distributed."""
    # Compute upper and lower bounds for the specified quantile. Then filter the data frame to fall within
    # those bounds.
    delta = (1 - quantile) / 2.0
    return f"output_df = output_df[(outut_df[{input_column}] < output_df[{input_column}].quantile({1 - delta})) & (output_df[{input_column}] > output_df[{input_column}].quantile({delta}))]"


def _drop_columns(input_df, input_column, column_insights=None, warning_name=None):
    return f"output_df=output_df.drop(columns=['{input_column}'])"


def _search_and_edit(
    input_df,
    input_column,
    column_insights=None,
    warning_name=None,
    str_from="?",
    str_to="",
):
    return f"output_df['{input_column}']=output_df['{input_column}'].str.replace('{str_from}', '{str_to}', regex=True)"


def _convert_regex_to_missing(
    input_df, input_column, column_insights=None, warning_name=None
):
    # Handle numeric_disguised_missing_value insight
    from_val = None
    to_val = None
    if column_insights and column_insights.get(
        InsightsInfo.NUMERIC_DISGUISED_MISSING_VALUE
    ):
        from_val, to_val = (
            column_insights.get(InsightsInfo.NUMERIC_DISGUISED_MISSING_VALUE),
            "NULL",
        )

    # Handle regression frequent target label
    if column_insights and column_insights.get(InsightsInfo.REGRESSION_FREQUENT_LABEL):
        from_val, to_val = (
            column_insights.get(InsightsInfo.REGRESSION_FREQUENT_LABEL),
            "NaN",
        )

    if from_val and to_val:
        dtype = str(input_df[input_column].dtype)
        if "int" in dtype:
            from_val = int(from_val)
        if "float" in dtype:
            from_val = float(from_val)
        code = replace([from_val], to_val, input_column)
        return code
    return "NOT IMPLEMENTED"


def _replace_rare_values(
    input_df, input_column, column_insights=None, warning_name=None
):
    rare_categories = get_rare_categories(input_df, input_column)
    code = f"rare_categories = {rare_categories}\n"

    if column_insights and column_insights.get(InsightsInfo.RARE_CATEGORIES):
        # TODO: show rare categories
        code += (
            f"value_to_replace = 0\n"
            if is_numeric_dtype(input_df[input_column])
            else f"value_to_replace = 'Other'\n"
        )
        code += f"frequencies = output_df['{input_column}'].value_counts(normalize=True, ascending=True)\n"
        code += f"threshold = frequencies[(frequencies.cumsum() > 0.1).idxmax()]\n"
        code += f"mapping = output_df['{input_column}'].map(frequencies)\n"
        code += f"output_df['{input_column}'] = output_df['{input_column}'].mask(mapping < threshold, value_to_replace)"
        return code
    return "NOT IMPLEMENTED"


def _drop_rare_target(
    input_df, input_column, target_insights_info=None, warning_name=None
):
    """
    Drop the rows with rare target values, the threshold of high target cardinality is set at 20. We retain up rows
    with target that has cardinality <=20.
    """
    if target_insights_info and (
        target_insights_info.get(InsightsInfo.RARE_TARGET_LABEL)
        or target_insights_info.get(InsightsInfo.IMBALANCED_CLASSES)
    ):
        rare_target_labels_to_drop = target_insights_info.get(
            InsightsInfo.RARE_TARGET_LABEL
        )
        if type(rare_target_labels_to_drop) != list:
            rare_target_labels_to_drop = [rare_target_labels_to_drop]
        df_type = str(input_df[input_column].dtype)
        rare_target_labels_to_drop = parse_and_retain_data_type(
            rare_target_labels_to_drop, df_type
        )
        code = f"rare_target_labels_to_drop = {rare_target_labels_to_drop}\n"
        code += f"output_df = output_df[~output_df['{input_column}'].isin(rare_target_labels_to_drop)]"
        return code
    return "NOT IMPLEMENTED"


def _replace_rare_target(
    input_df, input_column, target_insights_info=None, warning_name=None
):
    """Replace rare target values with Other, and a new number if it's numeric"""
    if (
        warning_name == TARGET_COLUMN_INSIGHTS_INFO[Insights.RARE_TARGET_LABEL]["name"]
        or warning_name
        == TARGET_COLUMN_INSIGHTS_INFO[Insights.IMBALANCED_CLASSES]["name"]
    ):
        if target_insights_info and target_insights_info.get(
            InsightsInfo.RARE_TARGET_LABEL
        ):
            if is_numeric_dtype(input_df[input_column]):
                # Replace with a new class that doesn't exist in the original column, take the max of the numeric column and add 1 to it to create the new class value
                replace_with = 1 + input_df[input_column].max()
            else:
                replace_with = "Other"
            df_type = str(input_df[input_column].dtype)
            rare_target_labels_to_replace = target_insights_info.get(
                InsightsInfo.RARE_TARGET_LABEL
            )
            if type(rare_target_labels_to_replace) != list:
                rare_target_labels_to_replace = [rare_target_labels_to_replace]
            rare_target_labels_to_replace = parse_and_retain_data_type(
                rare_target_labels_to_replace, df_type
            )
            code = f"#For numeric columns, we take the max of target column and plus one to it to create a new class. \n"
            code += f"replace_with = '{replace_with}' \n"
            code += f"rare_target_labels_to_replace = {rare_target_labels_to_replace}\n"
            code += f"output_df['{input_column}'] = output_df['{input_column}'].mask(output_df['{input_column}'].isin(rare_target_labels_to_replace), replace_with)"
            return code
    return "NOT IMPLEMENTED"


def _convert_to_numeric_and_drop_missing(
    input_df, input_column, target_insights_info=None, warning_name=None
):
    """"""
    if (
        target_insights_info
        and warning_name
        == TARGET_COLUMN_INSIGHTS_INFO[Insights.NON_NUMERIC_VALUES]["name"]
    ):
        code = f"output_df['{input_column}'] = pd.to_numeric(output_df['{input_column}'], errors='coerce') \n"
        code += f"output_df = output_df.dropna(subset=['{input_column}'])"
        return code
    return


OPERATOR_TO_TRANSFORM_FUNC_MAP = {
    # TODO: change to drop OPERATORS.DROP_ROWS
    OPERATORS.DROP_MISSING: drop_rows,
    OPERATORS.DROP_COLUMN: _drop_columns,
    OPERATORS.DROP_OUTLIERS: _drop_outliers_with_robust_std,
    OPERATORS.REPLACE_RARE_VALUES: _replace_rare_values,
    OPERATORS.CONVERT_REGEX_TO_MISSING: _convert_regex_to_missing,
    OPERATORS.SEARCH_AND_EDIT: _search_and_edit,
    OPERATORS.REPLACE_RARE_TARGET: _replace_rare_target,
    OPERATORS.DROP_RARE_TARGET: _drop_rare_target,
    OPERATORS.CONVERT_TO_NUMERIC_AND_DROP_MISSING: _convert_to_numeric_and_drop_missing,
    # OPERATORS.IMPUTE_MODE: impute_mode,
    OPERATORS.IMPUTE_MEDIAN: impute_median,
    OPERATORS.IMPUTE_MEAN: impute_mean,
    OPERATORS.IMPUTE_GENERIC: impute_generic,
    OPERATORS.IMPUTE_NAN: impute_nan,
}


def apply_transform(
    input_df: pd.DataFrame,
    operator_id: str,
    input_column: str,
    transform_name: str,
    warning_insight_id: str = None,
    column_insights=None,
    **kwargs,
):
    """
    Apply transform to the pandas DataFrame and return a transformed DataFrame and exportable code string
    param: input_df: a pandas DataFrame pending for update
    param: operator_id: operator identifier
    param: input_column: a column name to apply transform on the column
    param: transform_name: operator name
    param: warning_insight_id: id of the generated insight
    column_insights: data insights info which suggested the transform
    """
    warning_name = INSIGHTS_INFO_MAP[warning_insight_id]["name"]
    code = f"{chr(10)}# Code to {transform_name} for column: {input_column} to resolve warning: {warning_name} \n"
    column_insights_info = None
    if column_insights:
        for insight in column_insights:
            warning = insight.get("warnings")
            if warning_insight_id and warning:
                if warning.get("insight_id") == warning_insight_id:
                    column_insights_info = warning.get("info")
                    break
    code += OPERATOR_TO_TRANSFORM_FUNC_MAP[operator_id](
        input_df, input_column, column_insights_info, warning_name, **kwargs
    )
    code += "\n"
    exec_symbols = {"pd": pd, "output_df": input_df, "stats": stats, "np": np}

    exec(code, exec_symbols, exec_symbols)

    result = exec_symbols["output_df"]
    return code, result
