import json
import traceback
from collections import Counter
from enum import Enum
from typing import List

from .logging import ERROR
from .platform import APP_CONTEXT


class EventStatus(Enum):
    """
    API event status options for OE logging
    """

    START = "start"
    FAILED = "failed"
    SUCCESS = "success"


# ToDo: move "ganymede" to a const prefix variable
class MetricsEventType(Enum):
    """Event types for all backend structured logs"""

    IMPORT_SM_DW = "ganymede.import_sagemaker_dw"
    INITIALIZATION = "ganymede.initialization"
    LAZY_LOADED = "ganymede.lazy_loaded"

    APPLY_TRANSFORM = "ganymede.apply_transform"
    COMPUTE_TARGET_INSIGHTS = "ganymede.compute_target_insights"
    COMPUTE_COLUMN_INSIGHTS_DF = "ganymede.df.compute_column_insights"
    UPDATE_COMPUTE_ROW_COUNT = "ganymede.update_compute_row_count"

    ERROR = "ganymede.backend.error"
    UNEXPECTED_EVENT_TYPE = "ganymede.unexpected_event_type"
    UNEXPECTED_EVENT_PARAMETER = "ganymede.unexpected_event_parameter"


# Event metrics


def create_session_start_log():
    session_start_log = {
        "event_type": MetricsEventType.IMPORT_SM_DW.value,
        "app_context": APP_CONTEXT,
    }
    return json.dumps(session_start_log)


# ToDo: change to event_type: MetricsEventType
def create_event_metrics(event_type: str, event_status: EventStatus, metadata=None):
    request_metrics = {
        "event_type": event_type,
        "event_status": event_status.value,
        "app_context": APP_CONTEXT,
    }
    if metadata:
        request_metrics["metadata"] = metadata
    return json.dumps(request_metrics)


def get_apply_transform_metrics(
    warning_name, transform_name, operator_id, metadata=None
):
    request_metrics = {
        "event_type": MetricsEventType.APPLY_TRANSFORM.value,
        "warning_name": warning_name,
        "transform_name": transform_name,
        "operator_id": operator_id,
        "app_context": APP_CONTEXT,
    }
    if metadata:
        request_metrics["metadata"] = metadata
    return json.dumps(request_metrics)


def get_column_insights_metrics(data_quality_issues=[]):
    request_metrics = {
        "event_type": MetricsEventType.COMPUTE_COLUMN_INSIGHTS.value,
        "app_context": APP_CONTEXT,
        "data_quality_issues": data_quality_issues,
        "num_data_quality_issues": len(data_quality_issues)
        if data_quality_issues
        else 0,
    }
    return json.dumps(request_metrics)


def get_df_insights_metrics(df_column_insights):
    df_insights = []
    for _, insights in df_column_insights.items():
        if insights:
            df_insights.extend(
                [insights["warnings"]["insight_id"] for insights in insights]
            )
    request_metrics = {
        "event_type": MetricsEventType.COMPUTE_COLUMN_INSIGHTS_DF.value,
        "app_context": APP_CONTEXT,
        "num_data_quality_issues": len(df_insights),
        "data_quality_issues": Counter(df_insights),
    }
    return json.dumps(request_metrics)


def get_target_column_metrics(problem_type, data_quality_issues=[]):
    request_metrics = {
        "event_type": MetricsEventType.COMPUTE_TARGET_INSIGHTS.value,
        "problem_type": problem_type,
        "app_context": APP_CONTEXT,
        "num_data_quality_issues": len(data_quality_issues)
        if data_quality_issues
        else 0,
        "data_quality_issues": data_quality_issues,
    }
    return json.dumps(request_metrics)


def create_update_compute_row_count_metrics(row_count, column_count):
    request_metrics = {
        "event_type": MetricsEventType.UPDATE_COMPUTE_ROW_COUNT.value,
        "row_count": row_count,
        "column_count": column_count,
        "app_context": APP_CONTEXT,
    }
    return json.dumps(request_metrics)


# Error metrics


def create_structured_error_log(
    exception,
    event_type=None,
    message=None,
    error_type=MetricsEventType.ERROR.value,
    level=ERROR,
):
    error_log = {
        "level": level,
        "app_context": APP_CONTEXT,
        "event_type": event_type,
        "error_type": error_type,
        "error_name": None if not exception else type(exception).__name__,
        "message": message,
        "trusted_error_details": None
        if not exception
        else get_trusted_error_details(exception.__traceback__),
    }
    return json.dumps(error_log)


def get_trusted_error_details(tb) -> List[str]:
    """Return trusted error details with non-sensitive info"""
    stack_summary = traceback.extract_tb(tb)
    trusted_error_details = []
    for frame_summary in stack_summary:
        trusted_error_details.append(
            f"{frame_summary.filename}:{frame_summary.lineno}:{frame_summary.name}"
        )
    return trusted_error_details
