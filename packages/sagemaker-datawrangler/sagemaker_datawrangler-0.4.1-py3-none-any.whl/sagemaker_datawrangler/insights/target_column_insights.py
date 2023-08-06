import logging

import pandas as pd

from sagemaker_datawrangler.insights.data_quality_insights import ColumnInsight, Warning
from sagemaker_datawrangler.logging.logging import get_metrics_logger
from sagemaker_datawrangler.logging.metrics import (
    MetricsEventType,
    create_structured_error_log,
)

metrics_logger = get_metrics_logger()


def _group_multiple_target_insights(target_insight: list) -> list:
    """
    Convert multiple target insights into a single insight with aggregated information for each label
    """
    from sagemaker_data_insights.insights import Insights

    aggregated_insights = []

    skewed_target_label_info = []
    rare_target_label_info = []
    for insight in target_insight:
        if insight["warnings"]["name"] == Insights.IMBALANCED_CLASSES:
            skewed_target_insight = {
                "feature_name": insight["feature_name"],
                "operators": insight["operators"],
                "warnings": insight["warnings"],
            }
            skewed_target_label_info.append(insight["warnings"]["info"])
        elif insight["warnings"]["name"] == Insights.RARE_TARGET_LABEL:
            rare_target_label_insight = {
                "feature_name": insight["feature_name"],
                "operators": insight["operators"],
                "warnings": insight["warnings"],
            }
            rare_target_label_info.append(insight["warnings"]["info"])
        else:
            aggregated_insights.append(insight)

    if skewed_target_label_info:
        if len(skewed_target_label_info) == 1:
            skewed_target_insight["warnings"]["info"] = skewed_target_label_info[0]
        else:
            skewed_target_insight["warnings"] = {
                "insight_id": "sagemaker.data_quality.classes_too_imbalanced",
                "severity": "med_sev",
                "name": "Classes too imbalanced",
            }
            label = []
            count = []
            most_frequent_label = skewed_target_label_info[0]["most_frequent_label"]
            most_frequent_label_count = skewed_target_label_info[0][
                "most_frequent_label_count"
            ]

            for info in skewed_target_label_info:
                label.append(info["label"])
                count.append(info["count"])

            skewed_target_insight["warnings"]["info"] = {
                "label": label,
                "count": count,
                "most_frequent_label": most_frequent_label,
                "most_frequent_label_count": most_frequent_label_count,
            }
        # Process warning
        skewed_target_insight["warnings"] = vars(
            Warning(
                insight_id=skewed_target_insight["warnings"]["insight_id"],
                severity=skewed_target_insight["warnings"]["severity"],
                name=skewed_target_insight["warnings"]["name"],
                info=skewed_target_insight["warnings"]["info"],
            )
        )
        aggregated_insights.append(skewed_target_insight)

    if rare_target_label_info:
        if len(rare_target_label_info) == 1:
            rare_target_label_insight["warnings"]["info"] = rare_target_label_info[0]
        else:
            rare_target_label_insight["warnings"] = {
                "insight_id": "sagemaker.data_quality.too_few_instances_per_class",
                "severity": "high_sev",
                "name": "Too few instances per class",
            }
            label = []
            count = []
            for info in rare_target_label_info:
                label.append(info["label"])
                count.append(info["count"])
            rare_target_label_insight["warnings"]["info"] = {
                "label": label,
                "count": count,
            }

        rare_target_label_insight["warnings"] = vars(
            Warning(
                insight_id=rare_target_label_insight["warnings"]["insight_id"],
                severity=rare_target_label_insight["warnings"]["severity"],
                name=rare_target_label_insight["warnings"]["name"],
                info=rare_target_label_insight["warnings"]["info"],
            )
        )
        aggregated_insights.append(rare_target_label_insight)

    return aggregated_insights


def analyze_target(
    df: pd.DataFrame, problem_type: str, target_column_name: str
) -> dict:
    """
    Target column analyzers to run analysis on target column insights and recommend transforms

    Params:
        df: pd.DataFrame pandas data frame
        problem_type: str, Classfication or Regression
        target_column_name: str, name of the target column

    Returns:
        dict:
        target_column_name: a list of data insights with recommended transforms
        Example:
        {'target': [{'feature_name': 'target', 'warnings': {'name': 'Rare target label', 'insight_id': 'sagemaker.data_quality.rare_target_label', 'severity': 'high_sev', 'info': {'label': 'c', 'count': 15}, 'description': 'Rare target label'}, 'operators': [{'operator_id': 'sagemaker.spark.handle_outliers_0.1', 'transformer_name': 'Replace rare values'}]}, {'feature_name': 'target', 'warnings': {'name': 'Rare target label', 'insight_id': 'sagemaker.data_quality.rare_target_label', 'severity': 'high_sev', 'info': {'label': 'a', 'count': 5}, 'description': 'Rare target label'}, 'operators': [{'operator_id': 'sagemaker.spark.handle_outliers_0.1', 'transformer_name': 'Replace rare values'}]}]}
    """
    from sagemaker_data_insights.analyzers.target_column_analyzer import (
        analyze_target_classification,
        analyze_target_regression,
    )
    from sagemaker_data_insights.calc_stats_pandas_series import (
        _calc_stats_pandas_series,
    )
    from sagemaker_data_insights.const import TaskType

    from sagemaker_datawrangler.insights.data_quality_insights import (
        parse_column_insights,
    )

    if problem_type not in [TaskType.CLASSIFICATION, TaskType.REGRESSION]:
        metrics_logger.error(
            create_structured_error_log(
                exception=None,
                event_type=MetricsEventType.COMPUTE_TARGET_INSIGHTS.value,
                message=f"Invalid problem type {problem_type}",
            )
        )
        return

    if target_column_name not in list(df.columns):
        logging.warning(
            f"Target column {target_column_name} not found in the DataFrame"
        )
        return

    target_col_metrics = _calc_stats_pandas_series(df[target_column_name])

    target_analyzer = (
        analyze_target_regression
        if problem_type == TaskType.REGRESSION
        else analyze_target_classification
    )

    target_insights, _ = target_analyzer(df[target_column_name], target_col_metrics)

    parsed_insights = parse_column_insights(
        target_column_name, target_insights["insights"]
    )

    # Group multiple instances of the same target insight
    grouped_insights = _group_multiple_target_insights(parsed_insights)

    return {target_column_name: grouped_insights}
