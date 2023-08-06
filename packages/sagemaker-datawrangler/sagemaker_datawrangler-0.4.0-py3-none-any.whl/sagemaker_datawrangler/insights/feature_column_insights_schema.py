from sagemaker_datawrangler.transformers.constants import OPERATORS, TRANSFORMER_NAMES

from .insights_constants import Insights, InsightsInfo, InsightsSeverity

FEATURE_COLUMN_INSIGHTS_INFO = {
    Insights.HIGH_MISSING_RATIO: {
        "info_key": InsightsInfo.MISSING_VALUES,
        "name": "Missing values",
        "description": "The column has missing values such as None, NaN or NaT.",
        "severity": InsightsSeverity.HIGH,
        "operators": [
            {
                "operator_id": OPERATORS.IMPUTE_GENERIC,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_WITH_NEW_VALUE,
                "transform_description": 'Replaces missing values with the string that has the following value: "Other" if textual data and 0 if numerical data',
                "is_recommended": True,
            },
            {
                "operator_id": OPERATORS.DROP_MISSING,
                "transformer_name": TRANSFORMER_NAMES.DROP_MISSING,
                "transform_description": "Drops rows with missing values.",
            },
            {
                "operator_id": OPERATORS.DROP_COLUMN,
                "transformer_name": TRANSFORMER_NAMES.DROP_COLUMN,
                "transform_description": "Drops the column from the dataset.",
            },
            {
                "operator_id": OPERATORS.IMPUTE_MEDIAN,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_WITH_MEDIAN,
                "transform_description": "Replaces missing values with the median of the column.",
            },
            {
                "operator_id": OPERATORS.IMPUTE_MEAN,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_WITH_MEAN,
                "transform_description": "Replaces missing values with the mean of the column.",
            },
        ],
    },
    Insights.DISGUISED_MISSING_VALUES: {
        "info_key": InsightsInfo.DISGUISED_MISSING_VALUES,
        "name": "Disguised missing values",
        "severity": InsightsSeverity.LOW,
        "description": "The column has values that might represent a missing value. These values can be placeholders for missing data. "
        "We recommend replacing the values or dropping the rows containing them.",
        "example_prefix": "The following are examples of disguised missing values in the dataset: ",
        "operators": [
            {
                "operator_id": OPERATORS.IMPUTE_GENERIC,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_WITH_NEW_VALUE,
                "transform_description": 'Replaces missing values with the string that has the following value: "Other" if textual data and 0 if numerical data',
                "is_recommended": True,
            },
            {
                "operator_id": OPERATORS.DROP_MISSING,
                "transformer_name": TRANSFORMER_NAMES.DROP_MISSING,
                "transform_description": "Drops rows with missing values.",
            },
            {
                "operator_id": OPERATORS.IMPUTE_NAN,
                "transformer_name": TRANSFORMER_NAMES.CONVERT_DISGUISED_TO_MISSING,
                "transform_description": "Replaces disguised missing values with None.",
            },
        ],
    },
    Insights.NUMERIC_DISGUISED_MISSING_VALUE: {
        "info_key": InsightsInfo.NUMERIC_DISGUISED_MISSING_VALUE,
        "severity": InsightsSeverity.LOW,
        "name": "Disguised missing values",
        "description": "The column has a value that is very frequent and we suspect that it could indicate a missing value. Consider converting it to explicitly missing value.",
        "example_prefix": "The value which could be indicative of a missing value is ",
        "operators": [
            {
                "operator_id": OPERATORS.IMPUTE_NAN,
                "transformer_name": TRANSFORMER_NAMES.CONVERT_DISGUISED_TO_MISSING,
                "transform_description": "Replaces the value with None.",
            },
        ],
    },
    Insights.CATEGORICAL_RARE: {
        "info_key": InsightsInfo.RARE_CATEGORIES,
        "name": "Rare categories",
        "severity": InsightsSeverity.LOW,
        "description": "The column has some categories that are rare. Consider replacing the rare values with a generic string like Other or the most frequent category.",
        "example_prefix": "The count of rare categories together comprise of 10% of the total count. The following are the rare categories in your dataset ",
        "operators": [
            {
                "operator_id": OPERATORS.REPLACE_RARE_VALUES,
                "transformer_name": TRANSFORMER_NAMES.REPLACE_RARE_VALUES,
                "transform_description": 'Replaces rare values with the string that has the following value: "Other" if textual and "0" if numeric.',
            }
        ],
    },
    # TODO: implement this insight
    Insights.CATEGORICAL_TYPO_CORRECTION: {
        "name": "Categories with typos",
        "description": "Several categories in this column are very similar. It can be a potential misspelling. Consider applying spelling correction transform to fix them.",
        "example_prefix": "The typos are ",
        # TODO: implement this transform
        "severity": InsightsSeverity.LOW,
        "operators": [
            {
                "operator_id": OPERATORS.SEARCH_AND_EDIT,
                "transformer_name": TRANSFORMER_NAMES.CORRECT_TYPOS_IN_CATEGORIES,
                "transform_description": "Corrects potential typos in the category values.",
            }
        ],
    },
    Insights.CONSTANT_COLUMN: {
        "name": "Constant column",
        "description": "The column has only one value. It therefore has no predictive power. We recommend using the Drop column transform to drop it.",
        "severity": InsightsSeverity.HIGH,
        "operators": [
            {
                "operator_id": OPERATORS.DROP_COLUMN,
                "transformer_name": TRANSFORMER_NAMES.DROP_COLUMN,
                "transform_description": "Drops the column.",
                "is_recommended": True,
            }
        ],
    },
    Insights.ID_COLUMN: {
        "name": "ID column",
        "description": "The column has one unique value per row and therefore does not contribute to learnable insights. It is probably an ID column or database key. We strongly recommend dropping the column.",
        "severity": InsightsSeverity.HIGH,
        "operators": [
            {
                "operator_id": OPERATORS.DROP_COLUMN,
                "transformer_name": TRANSFORMER_NAMES.DROP_COLUMN,
                "transform_description": "Drops the column.",
                "is_recommended": True,
            }
        ],
    },
    Insights.HIGH_CARDINALITY: {
        "name": "High cardinality",
        "description": "The column has many unique values and may not contribute to learnable insights. Consider the importance of the column and possibily drop it.",
        "severity": InsightsSeverity.MEDIUM,
        "operators": [
            {
                "operator_id": OPERATORS.DROP_COLUMN,
                "transformer_name": TRANSFORMER_NAMES.DROP_COLUMN,
                "transform_description": "Drops the column.",
            }
        ],
    },
}
