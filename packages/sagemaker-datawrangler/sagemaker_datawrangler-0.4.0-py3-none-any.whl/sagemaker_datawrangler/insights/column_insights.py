import logging
import traceback
from copy import deepcopy

import pandas as pd
from joblib import Parallel, delayed

from sagemaker_datawrangler.logging.logging import get_metrics_logger
from sagemaker_datawrangler.logging.metrics import (
    MetricsEventType,
    create_structured_error_log,
)

from .data_quality_insights import (
    generate_column_insight_for_missing_ratio,
    generate_column_insights_based_on_unique_values,
    generate_disguised_missing_values_insight,
    parse_column_insights,
)
from .utils import get_column_highlights

metrics_logger = get_metrics_logger()


def get_df_column_insights(df: pd.DataFrame, selected_column_name: str = None):
    """
    Calculate a pandas DataFrame all columns' statistics, quality issues and recommended transforms.
    param: df: a pandas DataFrame
    """
    from sagemaker_data_insights.analyzers.feature_analyzer import (
        analyze_feature_column,
    )
    from sagemaker_data_insights.column_data_insights.column_insights_data import (
        get_column_insights_data,
    )

    from .parser import parse_column_statistics

    if selected_column_name and selected_column_name not in list(df.columns):
        # selected column name is no longer in the dataframe, return early
        return (
            {selected_column_name: {}},
            {selected_column_name: []},
            {selected_column_name: {}},
        )

    if selected_column_name:
        df = df[[selected_column_name]]

    def _compute(column_name, column_data: pd.Series):
        try:
            column_profiles, column_stats = get_column_insights_data(
                column_name, column_data
            )
            column_insights = []
            parsed_column_stats = parse_column_statistics(column_profiles, column_data)

            if column_profiles.get("logicalDataType") in ["numeric", "categorical"]:
                column_insights = analyze_feature_column(
                    column_data,
                    column_profiles.get("logicalDataType"),
                    column_stats[column_name],
                )
            if column_insights and column_insights.get("insights") is not None:
                column_insights = parse_column_insights(
                    column_name, column_insights["insights"], column_data
                )

            column_insights = [
                *column_insights,
                *generate_column_insight_for_missing_ratio(
                    column_statistics=parsed_column_stats,
                    column_name=column_name,
                ),
                *generate_disguised_missing_values_insight(
                    df, column_name=column_name, column_statistics=parsed_column_stats
                ),
                *generate_column_insights_based_on_unique_values(
                    df, column_name=column_name
                ),
            ]
        except Exception as exception:
            metrics_logger.error(
                create_structured_error_log(
                    exception=exception,
                    event_type=MetricsEventType.COMPUTE_COLUMN_INSIGHTS_DF.value,
                    message=f"Failed to profile column while computing insights",
                )
            )
            # reassign the initial values to column_stats and column_insights
            parsed_column_stats = {}
            column_insights = []

        return {
            "column_stats": parsed_column_stats,
            "column_insights": column_insights,
            "column_name": column_name,
            "column_highlights": get_column_highlights(
                column_name, column_data, deepcopy(column_insights)
            ),
        }

    compute_results = Parallel(n_jobs=-1)(
        delayed(_compute)(column_name, column_data)
        for column_name, column_data in df.items()
    )
    # collect and return insights results
    df_column_statistics = {}
    df_column_insights = {}
    df_column_highlights = {}

    for result in compute_results:
        df_column_statistics[result["column_name"]] = result["column_stats"]
        df_column_insights[result["column_name"]] = result["column_insights"]
        df_column_highlights[result["column_name"]] = result["column_highlights"]

    return df_column_statistics, df_column_insights, df_column_highlights
