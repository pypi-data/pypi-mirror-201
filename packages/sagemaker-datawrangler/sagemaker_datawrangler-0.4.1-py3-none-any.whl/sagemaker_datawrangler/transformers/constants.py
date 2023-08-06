class OPERATORS:
    DROP_MISSING = "sagemaker.pandas.drop_missing"
    IMPUTE_MISSING_CATEGORICAL = "sagemaker.pandas.impute_missing_categorical"
    IMPUTE_MISSING_NUMERIC = "sagemaker.pandas.impute_missing_numeric"
    DROP_COLUMN = "sagemaker.pandas.drop_column"
    REPLACE_RARE_VALUES = "sagemaker.pandas.replace_rare_values"
    CONVERT_REGEX_TO_MISSING = "sagemaker.pandas.convert_regex_to_missing"
    SEARCH_AND_EDIT = "sagemaker.pandas.search_and_edit"
    DROP_OUTLIERS = "sagemaker.pandas.drop_outliers"

    # Handle Missing operators
    # IMPUTE_MODE = "sagemaker.pandas.impute_mode"
    IMPUTE_MEDIAN = "sagemaker.pandas.impute_median"
    IMPUTE_MEAN = "sagemaker.pandas.impute_mean"
    IMPUTE_GENERIC = "sagemaker.pandas.impute_generic"
    IMPUTE_NAN = "sagemaker.pandas.impute_nan"

    # Target operators
    REPLACE_RARE_TARGET = "sagemaker.pandas.replace_rare_target"
    DROP_RARE_TARGET = "sagemaker.pandas.drop_rare_target"
    CONVERT_TO_NUMERIC_AND_DROP_MISSING = (
        "sagemaker.pandas.convert_to_numeric_and_drop_missing"
    )


ROW_BASED_TRANSFORMERS = [
    "Drop missing",
    "Drop rare target values",
    "Convert to numeric and drop NaN",
]


class TRANSFORMER_NAMES:
    CONVERT_DISGUISED_TO_MISSING = "Convert disguised to missing"
    CONVERT_TO_NUMERIC_AND_DROP_NAN = "Convert to numeric and drop NaN"
    CORRECT_TYPOS_IN_CATEGORIES = "Correct typos in categories"
    DROP_COLUMN = "Drop column"
    DROP_MISSING = "Drop missing"
    DROP_RARE_TARGET_VALUES = "Drop rare target values"
    HANDLE_NUMERIC_OUTLIERS = "Handle numeric outliers"
    REPLACE_RARE_TARGET_VALUES = "Replace rare target values"
    REPLACE_RARE_VALUES = "Replace rare values"
    REPLACE_WITH_MEAN = "Replace with mean"
    REPLACE_WITH_MEDIAN = "Replace with median"
    REPLACE_WITH_NAN = "Replace with NaN"
    REPLACE_WITH_NEW_VALUE = "Replace with new value"
