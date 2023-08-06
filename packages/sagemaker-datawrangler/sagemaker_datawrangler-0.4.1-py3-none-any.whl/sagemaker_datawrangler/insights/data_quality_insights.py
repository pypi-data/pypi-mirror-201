from typing import List

import pandas as pd

from sagemaker_datawrangler.transformers.utils import get_rare_categories

from .feature_column_insights_schema import FEATURE_COLUMN_INSIGHTS_INFO
from .insights_constants import (
    Insights,
    InsightsInfo,
    InsightsSeverity,
    InsightsThresholds,
)
from .target_column_insights_schema import TARGET_COLUMN_INSIGHTS_INFO
from .utils import get_transforms_for_missing_insights, parse_insight_id, set_examples

INSIGHTS_INFO_MAP = {**FEATURE_COLUMN_INSIGHTS_INFO, **TARGET_COLUMN_INSIGHTS_INFO}
INSIGHTS_TO_REMOVE = [
    Insights.TARGET_OUTLIERS,
    Insights.SKEWED_TARGET,
    Insights.HEAVY_TAILED_TARGET,
    Insights.NUMERIC_DISGUISED_MISSING_VALUE,
    Insights.CATEGORICAL_RARE,
]


class Warning(object):
    # TODO: Define Map with all supported warnings

    def __init__(
        self, insight_id: str, severity: str = None, name: str = None, info: dict = None
    ):
        insight_info = INSIGHTS_INFO_MAP.get(insight_id)
        self.insight_id = insight_id
        self.severity = severity if severity else insight_info.get("severity")
        self.info = info
        self.name = name

        if insight_info:
            self.description = insight_info.get("description")
            self.name = insight_info.get("name", name)
            info_key = insight_info.get("info_key")
            if info and info_key:
                values = self.info.get(info_key)
                self.example = set_examples(insight_info.get("example_prefix"), values)


class ColumnInsight(object):
    def __init__(self, feature_name: str, warnings: Warning, operators=None):
        self.feature_name = feature_name
        self.warnings = vars(warnings)
        self.operators = (
            INSIGHTS_INFO_MAP[warnings.insight_id]["operators"]
            if not operators
            else operators
        )


def generate_column_insight_for_missing_ratio(column_statistics, column_name):
    missing_ratio = column_statistics["missingRatio"]
    if missing_ratio == 0:
        return []

    recommended_transforms = get_transforms_for_missing_insights(
        column_statistics, missing_ratio
    )
    warning = Warning(
        insight_id=Insights.HIGH_MISSING_RATIO,
        info={InsightsInfo.MISSING_VALUES: [None]},
    )
    column_insights = vars(
        ColumnInsight(
            feature_name=column_name, warnings=warning, operators=recommended_transforms
        )
    )
    return [column_insights]


def generate_disguised_missing_values_insight(df, column_name, column_statistics):
    unique_values = df[column_name].unique()
    disguised_missing_values = []

    for value in unique_values:
        if isinstance(value, str):
            # handle cases where there are leading or trailing spaces for common missing values
            if value.upper().strip() in InsightsThresholds.DISGUISED_MISSING_VALUES:
                disguised_missing_values.append(value)
    if disguised_missing_values:
        recommended_transforms = get_transforms_for_missing_insights(
            column_statistics, insight=Insights.DISGUISED_MISSING_VALUES
        )
        warning = Warning(
            insight_id=Insights.DISGUISED_MISSING_VALUES,
            severity=InsightsSeverity.MEDIUM_FEATURE,
            info={
                InsightsInfo.DISGUISED_MISSING_VALUES: list(disguised_missing_values)
            },
        )
        column_insights = vars(
            ColumnInsight(
                feature_name=column_name,
                warnings=warning,
                operators=recommended_transforms,
            )
        )
        return [column_insights]
    return []


def generate_column_insights_based_on_unique_values(df, column_name):
    n_unique, n_rows = len(pd.unique(df[column_name])), df[column_name].size
    column_insights = None
    if n_unique == 1:
        warning = Warning(
            insight_id=Insights.CONSTANT_COLUMN,
        )
        column_insights = vars(
            ColumnInsight(feature_name=column_name, warnings=warning)
        )
    elif n_unique == n_rows:
        warning = Warning(
            insight_id=Insights.ID_COLUMN,
        )
        column_insights = vars(
            ColumnInsight(feature_name=column_name, warnings=warning)
        )
    elif n_unique / n_rows > InsightsThresholds.HIGH_CARDINALITY:
        warning = Warning(insight_id=Insights.HIGH_CARDINALITY)
        column_insights = vars(
            ColumnInsight(feature_name=column_name, warnings=warning)
        )
    return [column_insights] if column_insights else []


def parse_column_insights(
    column_name: str, insights: List, column_data: pd.Series = None
):
    """
    Parse the raw column insights data for frontend usage
    Related logic in DW: https://tiny.amazon.com/102mzxuy8/githawssageblobmastsrcsage
    param: column_name: DataFrame column name (unique) e.g. 'boat'
    param: column_insights: an array of insights of the column from SageMakerDataInsights
    """
    parsed_column_insights = []
    for insight in insights:
        insight_id = parse_insight_id(insight["key"])

        # Remove Outliers in target, Skewness in target, Heavy tailed target
        if insight_id in INSIGHTS_TO_REMOVE:
            continue
        # temporary as data insights does not return rare categories correctly
        if insight_id == Insights.CATEGORICAL_RARE and column_data is not None:
            insight["info"] = {}
            insight_info_key = INSIGHTS_INFO_MAP.get(insight_id).get("info_key")
            insight["info"][insight_info_key] = get_rare_categories(
                pd.DataFrame({column_name: column_data}), column_name
            )
        warning = Warning(
            insight_id=insight_id,
            severity=insight["severity"],
            info=insight.get("info"),
            name=insight["key"],
        )
        column_insights = vars(
            ColumnInsight(feature_name=column_name, warnings=warning)
        )
        parsed_column_insights.append(column_insights)
    return parsed_column_insights
