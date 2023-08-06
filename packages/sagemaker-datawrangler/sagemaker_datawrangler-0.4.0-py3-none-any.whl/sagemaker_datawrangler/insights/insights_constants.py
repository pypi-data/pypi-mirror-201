MAX_EXAMPLES_TO_DISPLAY = 10


class Insights:
    """
    Insights supported in Ganymede
    """

    # feature column insights
    HIGH_MISSING_RATIO = "sagemaker.data_quality.high_missing_ratio"
    DISGUISED_MISSING_VALUES = "sagemaker.data_quality.disguised_missing_values"
    CATEGORICAL_RARE = "sagemaker.data_quality.categorical_rare_categories"
    CATEGORICAL_TYPO_CORRECTION = "sagemaker.data_quality.categorical_typo_correction"
    CONSTANT_COLUMN = "sagemaker.data_quality.constant_column"
    ID_COLUMN = "sagemaker.data_quality.id_column"
    HIGH_CARDINALITY = "sagemaker.data_quality.high_cardinality"

    # target column insights
    # Regression
    REGRESSION_FREQUENT_LABEL = "sagemaker.data_quality.regression_frequent_label"
    NON_NUMERIC_VALUES = "sagemaker.data_quality.non_numeric_values"
    # Classification
    RARE_TARGET_LABEL = "sagemaker.data_quality.too_few_instances_per_class"
    HIGH_TARGET_CARDINALITY = "sagemaker.data_quality.high_target_cardinality"
    IMBALANCED_CLASSES = "sagemaker.data_quality.classes_too_imbalanced"
    HIGHLY_SKEWED_MINORITY = "sagemaker.data_quality.very_small_minority_class"

    # Insights excluded in GA:
    SKEWED_TARGET = "sagemaker.data_quality.skewed_target"
    HEAVY_TAILED_TARGET = "sagemaker.data_quality.heavy_tailed_target"
    TARGET_OUTLIERS = "sagemaker.data_quality.target_outliers"
    NUMERIC_DISGUISED_MISSING_VALUE = (
        "sagemaker.data_quality.numeric_disguised_missing_value"
    )


class InsightsSeverity:
    """
    Severity of data quality insights as defined in DataInsights
    """

    # High severity insights indicate a probable issue in the data. There should be very few false
    # positive high severity insights. It is recommended to highlight these warnings
    HIGH = "high_sev"

    # Medium severity insights indicate a possible issue with the data. By design, many of these
    # insights are false positive
    MEDIUM = "med_sev"

    # Low severity insights are either not important or with low confidence. Generally, they should
    # not be presented and are included here for completeness
    LOW = "low_sev"

    # This is a medium sev insight for a feature. Should be considered medium
    # severity if the feature is important (e.g. if the feature is in top 5 most important features) and as low
    # severity otherwise
    MEDIUM_FEATURE = "med_sev_feature"


class InsightsInfo:
    """
    Info contained within insights
    """

    MISSING_VALUES = "missing_values"
    DISGUISED_MISSING_VALUES = "potentially_missing_values"
    RARE_CATEGORIES = "rare_categories"
    NUMERIC_DISGUISED_MISSING_VALUE = "value"

    # https://github.com/aws/sagemaker-data-insights/blob/main/src/sagemaker_data_insights/insights.py#L85-L91
    IMBALANCED_CLASSES = "label"
    RARE_TARGET_LABEL = "label"
    FREQUENT_VALUE = "value"
    TARGET_CARDINALITY = "cardinality"
    MOST_FREQUENT_LABEL = "most_frequent_label"
    REGRESSION_FREQUENT_LABEL = "label"
    NON_NUMERIC_VALUES = "values"
    TARGET_FEW_OUTLIERS = ""
    HEAVY_TAILED_TARGET = ""
    HIGHLY_SKEWED_MINORITY = "label"


class InsightsThresholds:
    """
    Thresholds that have been defined for insights
    """

    from sagemaker_data_insights.insights import Insights

    HIGH_MISSING_RATIO = 0.5
    DISGUISED_MISSING_VALUES = {
        "UNKNOWN",
        "UNK",
        "",
        "NA",
        "N/A",
        "NULL",
        "MISSING",
        "?",
        "??",
        "???",
        "-",
        "NAN",
        "TBD",
    }
    TARGET_CARDINALITY_THRESHOLD = Insights.HIGH_TARGET_CARDINALITY_THRESHOLD - 1
    HIGH_CARDINALITY = 0.9
