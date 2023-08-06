from sagemaker_datawrangler.transformers.constants import OPERATORS, TRANSFORMER_NAMES

from .insights_constants import Insights, InsightsInfo, InsightsSeverity

# Insights related to target column
TARGET_COLUMN_INSIGHTS_INFO = {
    Insights.SKEWED_TARGET: {
        "name": "Skewness in target",
        "description": "The target column has a univariate distribution. The distribution might be skewed. Consider dropping the outliers.",
        "severity": InsightsSeverity.HIGH,
        "operators": [
            {
                "operator_id": OPERATORS.DROP_OUTLIERS,
                "transformer_name": TRANSFORMER_NAMES.HANDLE_NUMERIC_OUTLIERS,
                "transform_description": "Drops numeric values that are three standard errors away from the mean.",
            }
        ],
    },
    Insights.RARE_TARGET_LABEL: {
        "info_key": InsightsInfo.RARE_TARGET_LABEL,
        "name": "Too few instances per class",
        "description": "The target column has categories that appear rarely. You can replace the categories with the string, 'Other'. For numeric values, consider replacing them with a new number that does not exist in the target column.",
        "severity": InsightsSeverity.HIGH,
        "example_prefix": "The following are the rare categories in the target column ",
        "operators": [
            {
                "operator_id": OPERATORS.REPLACE_RARE_TARGET,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_RARE_TARGET_VALUES,
                "transformer_description": "Replaces rare target values with 'Other' or a new number.",
            },
            {
                "operator_id": OPERATORS.DROP_RARE_TARGET,
                "transformer_name": TRANSFORMER_NAMES.DROP_RARE_TARGET_VALUES,
                "transformer_description": "Drops rare target values whose count is less than 10.",
            },
        ],
    },
    Insights.HIGH_TARGET_CARDINALITY: {
        "info_key": InsightsInfo.TARGET_CARDINALITY,
        "name": "Too many classes",
        "severity": InsightsSeverity.LOW,
        "description": "There are many classes in the target column. Having many classes may result in longer training time or poor predicative quality. You may consider converting it to a regression task.",
        "example_prefix": "The number of classes in the target column is ",
        "operators": [],
    },
    Insights.IMBALANCED_CLASSES: {
        "info_key": InsightsInfo.IMBALANCED_CLASSES,
        "name": "Classes too imbalanced",
        "severity": InsightsSeverity.MEDIUM,
        "description": "There are categories in your dataset that appear much more frequently than other categories. The class imbalance might affect prediction accuracy. For accurate predictions, we recommend updating the dataset with rows that have the categories that appear less frequently.",
        "example_prefix": "The infrequent labels are ",
        "operators": [
            {
                "operator_id": OPERATORS.REPLACE_RARE_TARGET,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_RARE_TARGET_VALUES,
                "transform_description": "Replace rare target values with 'Other', or a new number.",
            },
            {
                "operator_id": OPERATORS.DROP_RARE_TARGET,
                "transformer_name": TRANSFORMER_NAMES.DROP_RARE_TARGET_VALUES,
                "transform_description": "Drop rare target values whose count is less than 1% of the target column.",
            },
        ],
    },
    Insights.HIGHLY_SKEWED_MINORITY: {
        "info_key": InsightsInfo.HIGHLY_SKEWED_MINORITY,
        "name": "Highly skewed minority",
        "severity": InsightsSeverity.HIGH,
        "description": "The minority label count is very low. The skew might affect prediction accuracy. For accurate predictions, we recommend upsampling or synthetic sampling using SMOTE.",
        "example_prefix": "The minority label is ",
        "operators": [],
    },
    Insights.REGRESSION_FREQUENT_LABEL: {
        "info_key": InsightsInfo.REGRESSION_FREQUENT_LABEL,
        "name": "Frequent label",
        "description": "The frequency of the label in the target column is uncommon for regression tasks. This could point to bugs in data collection or processing. In some cases, the very frequent label is a default value or a placeholder to indicate missing values. If that's the case, consider replace the value with NaN.",
        "example_prefix": "The frequent label is ",
        "severity": InsightsSeverity.MEDIUM,
        "operators": [
            {
                "operator_id": OPERATORS.CONVERT_REGEX_TO_MISSING,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_WITH_NAN,
                "transformer_description": "Replace categories that can't be converted to numeric values with NaNs",
            }
        ],
    },
    Insights.HEAVY_TAILED_TARGET: {
        "name": "Heavy tailed target",
        "description": "The target column is heavy tailed and contains outliers.",
        "severity": InsightsSeverity.MEDIUM,
    },
    Insights.NON_NUMERIC_VALUES: {
        "info_key": InsightsInfo.NON_NUMERIC_VALUES,
        "name": "Many non-numeric values",
        "description": "There are some categories in the target column can't be converted to numeric values. There might be data entry errors. We recommend removing the rows containing the values that can't be converted from the dataset.",
        "severity": InsightsSeverity.HIGH,
        "example_prefix": "The non numeric values are ",
        "operators": [
            {
                "operator_id": OPERATORS.CONVERT_TO_NUMERIC_AND_DROP_MISSING,
                "transformer_name": TRANSFORMER_NAMES.CONVERT_TO_NUMERIC_AND_DROP_NAN,
                "transform_description": "Convert invalid numerical values to NaN and drop. ",
            },
        ],
    },
    Insights.TARGET_OUTLIERS: {
        "name": "Outliers in target",
        "description": "The target column has several outliers. We recommend dropping them for more accurate predictions.",
        "severity": InsightsSeverity.MEDIUM,
        "operators": [
            {
                "operator_id": OPERATORS.DROP_OUTLIERS,
                "transformer_name": TRANSFORMER_NAMES.HANDLE_NUMERIC_OUTLIERS,
                "transform_description": "Drops numeric values that are three standard errors away from the mean.",
            }
        ],
    },
}
