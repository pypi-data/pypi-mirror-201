#!/usr/bin/env python
# coding: utf-8

# Copyright (c) me.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

import json
import logging
import time

import pandas as pd
from ipywidgets import DOMWidget
from traitlets import Bool, Enum, Unicode

from sagemaker_datawrangler.insights.target_column_insights import analyze_target

from ._frontend import module_name, module_version
from .config.config import COMPUTE_ON_ALL_ROWS, DEFAULT_MAX_COMPUTE_ROW_COUNT
from .datatable.df_converter import create_df_json_obj, is_valid_df_json
from .datatable.df_sort import (
    sort_df_rows_by_cell_highlight_count,
    sort_df_rows_by_highlight_in_the_column,
)
from .insights.column_insights import get_df_column_insights
from .insights.utils import is_table_level_transform
from .logging.logging import get_metrics_logger
from .logging.metrics import (
    EventStatus,
    MetricsEventType,
    create_event_metrics,
    create_structured_error_log,
    create_update_compute_row_count_metrics,
    get_apply_transform_metrics,
    get_column_insights_metrics,
    get_df_insights_metrics,
    get_target_column_metrics,
)
from .transformers.transformer import apply_transform
from .validators.event_validator import (
    is_valid_column_name,
    is_valid_operator_id,
    is_valid_problem_type,
    is_valid_transform_name,
    is_valid_warning_insight_id,
)

DEFAULT_OBJECT = {}

metrics_logger = get_metrics_logger()


class DataWranglerWidget(DOMWidget):
    """
    DataWrangler widget is an interactive data preparation widget in SageMaker Studio Notebook to automatically
    generate key visualizations, insights and recommended transforms on top of Pandas DataFrame.
    """

    _model_name = Unicode("DataWranglerModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("DataWranglerView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    _is_valid_df_json = Bool(True).tag(sync=True)
    _compute_status = Enum(
        ["idle", "busy"],
        default_value="idle",
    ).tag(sync=True)
    _df_json = Unicode("").tag(sync=True)

    _df_column_statistics = Unicode(json.dumps(DEFAULT_OBJECT)).tag(sync=True)
    _df_column_insights = Unicode(json.dumps(DEFAULT_OBJECT)).tag(sync=True)
    _df_target_column_insights = Unicode(json.dumps(DEFAULT_OBJECT)).tag(sync=True)
    # TODO: verify rare values when int remain int
    _df_column_highlights = Unicode(json.dumps(DEFAULT_OBJECT)).tag(sync=True)
    _transformer_code = Unicode("").tag(sync=True)

    _error_response = Unicode("").tag(sync=True)

    def __init__(self, df_origin: pd.DataFrame, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.info(
            f"DataFrame size: row_count = {len(df_origin)}, column_count = {len(df_origin.columns)}."
        )

        # register a callback for custom messages
        self.on_msg(self._received_message_handler)

        if COMPUTE_ON_ALL_ROWS == str(False):
            logging.info(
                f"Computing on the top {DEFAULT_MAX_COMPUTE_ROW_COUNT} rows of the DataFrame."
            )
            df = df_origin.head(DEFAULT_MAX_COMPUTE_ROW_COUNT)
        else:
            logging.info(f"Computing on all {len(df_origin)} rows of the DataFrame.")

        self._df_json_obj = DEFAULT_OBJECT

        self._df_column_statistics_obj = DEFAULT_OBJECT
        self._df_column_insights_obj = DEFAULT_OBJECT
        self._df_target_column_insights_obj = DEFAULT_OBJECT
        self._df_column_highlights_obj = DEFAULT_OBJECT

        self._error_response = json.dumps(DEFAULT_OBJECT)

        self._target_column_name = None

        self._update_df_and_json(df)

    def _update_df_and_json(self, df: pd.DataFrame) -> None:
        self._df = df.copy(deep=True)

        self._df_json_obj = create_df_json_obj(df)
        self._df_json = json.dumps(self._df_json_obj, default=str)
        self._is_valid_df_json = is_valid_df_json(self._df_json_obj)

    def _update_column_statistics(self, df_column_statistics_obj: dict) -> None:
        self._df_column_statistics_obj.update(df_column_statistics_obj)
        self._df_column_statistics = json.dumps(
            self._df_column_statistics_obj, default=str
        )

    def _update_column_insights(self, df_column_insights_obj: dict) -> None:
        self._df_column_insights_obj.update(df_column_insights_obj)
        self._df_column_insights = json.dumps(self._df_column_insights_obj, default=str)

    def _update_target_column_insights(self, df_target_column_insights: dict) -> None:
        self._df_target_column_insights_obj.update(df_target_column_insights)
        self._df_target_column_insights = json.dumps(
            self._df_target_column_insights_obj
        )

    def _update_column_highlights(self, df_column_highlights_obj: dict) -> None:
        self._df_column_highlights_obj.update(df_column_highlights_obj)
        self._df_column_highlights = json.dumps(
            self._df_column_highlights_obj, default=str
        )

    def _update_df_insights(self, df: pd.DataFrame) -> None:
        (
            df_column_statistics,
            df_column_insights,
            df_column_highlights,
        ) = get_df_column_insights(df)

        logging.info(get_df_insights_metrics(df_column_insights))

        self._df_column_insights_obj = df_column_insights
        self._df_column_statistics_obj = df_column_statistics
        self._df_column_highlights_obj = df_column_highlights

        self._df_column_statistics = json.dumps(
            self._df_column_statistics_obj, default=str
        )
        self._df_column_insights = json.dumps(self._df_column_insights_obj, default=str)
        self._df_column_highlights = json.dumps(
            self._df_column_highlights_obj, default=str
        )

    def _update_insights_on_transform(
        self, column_name: str, transform_name: str, new_df: pd.DataFrame
    ):
        """
        Update statistics and insights for dataframe or a single column depending on if the transform operates row-wise
        """
        if column_name and not is_table_level_transform(
            transform_name, previous_df=self._df, updated_df=new_df
        ):
            (
                df_column_statistics,
                df_column_insights,
                df_column_highlights,
            ) = get_df_column_insights(new_df, selected_column_name=column_name)
        else:
            (
                df_column_statistics,
                df_column_insights,
                df_column_highlights,
            ) = get_df_column_insights(new_df)

        self._update_column_statistics(df_column_statistics)
        self._update_column_insights(df_column_insights)
        self._update_column_highlights(df_column_highlights)

    def _update_df_to_be_sorted(self, df, df_column_highlights):
        sorted_df = sort_df_rows_by_cell_highlight_count(df, df_column_highlights)
        self._update_df_and_json(sorted_df)

    def _update_error_response(self, event, error_message, data={}) -> None:
        self._error_response = json.dumps(
            {
                "event": event,
                "error_message": error_message,
                "data": data,
            }
        )

    def _clean_error_response(self) -> None:
        self._error_response = json.dumps(DEFAULT_OBJECT)

    def _update_target_insights_on_transform(
        self, column_name: str, new_df: pd.DataFrame, problem_type: str
    ):
        """
        Update target column insights
        """
        target_insights = analyze_target(new_df, problem_type, column_name)
        self._update_target_column_insights(target_insights)

    def _received_message_handler(self, widget, content, buffers) -> None:
        self._clean_error_response()

        # Note: don't change these key names, otherwise will lost log keywords' consistency
        event_to_func_map = {
            "apply_transform": self._apply_transform,
            "compute_target_column_insights": self._compute_target_column_insights,
            "on_initial_render": self._on_initial_render,
            "log_frontend_version": self._log_frontend_version,
            "select_column": self._sort_insights,
        }
        event = content["event"]

        # parameters validation
        if event not in event_to_func_map:
            metrics_logger.error(
                create_structured_error_log(
                    exception=None,
                    event_type=MetricsEventType.UNEXPECTED_EVENT_TYPE.value,
                    message=f"Unexpected event type.",
                )
            )
            return

        start_time = time.time()
        logging.info(create_event_metrics(event, EventStatus.START))
        event_status = event_to_func_map[event](content)
        latency = time.time() - start_time
        logging.info(
            create_event_metrics(event, event_status, metadata={"latency": latency})
        )

    def update_compute_row_count(
        self, input_df: pd.DataFrame, row_count: int = -1
    ) -> None:
        self._clean_error_response()
        event_type = "update_compute_row_count"
        start_time = time.time()
        logging.info(create_event_metrics(event_type, EventStatus.START))

        self._compute_status = "busy"
        if row_count != -1:
            self._df = input_df.head(row_count)
            logging.info(f"Computing on the top {row_count} rows of the DataFrame.")
        else:
            self._df = input_df
            logging.info(f"Computing on all {len(self._df)} rows of the DataFrame.")

        try:
            self._update_df_insights(self._df)
        except Exception as exception:
            error_message = f"Data Wrangler can't compute the insights successfully. Use the following error message to help resolve the issue."
            metrics_logger.error(
                create_structured_error_log(
                    exception=exception,
                    event_type=MetricsEventType.UPDATE_COMPUTE_ROW_COUNT.value,
                    message=error_message,
                )
            )
            latency = time.time() - start_time
            logging.info(
                create_event_metrics(
                    event_type, EventStatus.FAILED, metadata={"latency": latency}
                )
            )
            self._update_error_response(event_type, f"{error_message}: {exception}")
        else:
            create_update_compute_row_count_metrics(
                row_count=len(self._df), column_count=len(self._df.columns)
            )
            latency = time.time() - start_time
            logging.info(
                create_event_metrics(
                    event_type, EventStatus.SUCCESS, metadata={"latency": latency}
                )
            )
        finally:
            self._compute_status = "idle"

    # Event handler functions:
    # ToDo: move to their own event handler files

    def _apply_transform(self, content) -> EventStatus:
        try:
            event_type = content["event"]

            column_name = content["data"]["column_name"]
            operator_id = content["data"]["operator_id"]
            transform_name = content["data"]["transform_name"]
            warning_insight_id = content["data"]["warning_insight_id"]
            is_target_insights = content["data"]["is_target_insight"]
            problem_type = content["data"]["problem_type"]

            # parameters validation
            if (
                not is_valid_column_name(column_name, self._df)
                or not is_valid_operator_id(operator_id)
                or not is_valid_transform_name(transform_name)
                or not is_valid_warning_insight_id(warning_insight_id)
                or not is_valid_problem_type(problem_type)
            ):
                metrics_logger.error(
                    create_structured_error_log(
                        exception=None,
                        event_type=MetricsEventType.UNEXPECTED_EVENT_PARAMETER.value,
                        message=f"Unexpected event parameter in event {event}.",
                    )
                )
                return EventStatus.FAILED

            if is_target_insights:
                column_insights = self._df_target_column_insights_obj.get(column_name)
            else:
                column_insights = self._df_column_insights_obj.get(column_name)

            code, output_df = apply_transform(
                self._df,
                operator_id,
                column_name,
                transform_name,
                warning_insight_id,
                column_insights,
            )
            logging.info(
                get_apply_transform_metrics(
                    warning_insight_id, transform_name, operator_id
                )
            )

            self._update_df_and_json(output_df)
            self._transformer_code = code

            self._update_insights_on_transform(
                column_name=column_name, transform_name=transform_name, new_df=output_df
            )

            if is_target_insights or self._target_column_name == column_name:
                self._update_target_insights_on_transform(
                    column_name=column_name, new_df=output_df, problem_type=problem_type
                )

        except Exception as exception:
            error_message = f"Data Wrangler couldn't apply the {transform_name} transform successfully. Use the following message to help fix the issue"
            metrics_logger.error(
                create_structured_error_log(
                    exception=exception,
                    event_type=MetricsEventType.APPLY_TRANSFORM.value,
                    message=f"{error_message}: {warning_insight_id}",
                )
            )
            self._update_error_response(
                event_type,
                f"{error_message}: {exception}",
                {
                    "column_name": column_name,
                    "operator_id": operator_id,
                    "transformer_name": transform_name,
                    "warning_insight_id": warning_insight_id,
                    "is_target_column": is_target_insights,
                },
            )

            return EventStatus.FAILED

        else:
            return EventStatus.SUCCESS

    def _compute_target_column_insights(self, content) -> EventStatus:
        try:
            event_type = content["event"]

            target_column_name = content["data"]["column_name"]
            self._target_column_name = target_column_name
            problem_type = content["data"]["problem_type"]

            # parameters validation
            if not is_valid_column_name(
                target_column_name, self._df
            ) or not is_valid_problem_type(problem_type):
                metrics_logger.error(
                    create_structured_error_log(
                        exception=None,
                        event_type=MetricsEventType.UNEXPECTED_EVENT_PARAMETER.value,
                        message=f"Unexpected event parameter in event {event_type}.",
                    )
                )
                return EventStatus.FAILED

            target_column_insights = analyze_target(
                self._df, problem_type, target_column_name
            )

            if target_column_insights.get("target"):
                logging.info(
                    get_target_column_metrics(
                        problem_type, len(target_column_insights["target"])
                    )
                )

            self._update_target_column_insights(target_column_insights)
        except Exception as exception:
            error_message = f"Data Wrangler can't compute the {target_column_insights} insights successfully. Use the following error message to help resolve the issue"
            metrics_logger.error(
                create_structured_error_log(
                    exception=exception,
                    event_type=MetricsEventType.COMPUTE_TARGET_INSIGHTS.value,
                    message=error_message,
                )
            )
            self._update_error_response(event_type, f"{error_message}: {exception}")

            return EventStatus.FAILED

        else:
            return EventStatus.SUCCESS

    def _on_initial_render(self, content) -> EventStatus:
        try:
            event_type = content["event"]

            self._update_df_insights(self._df)
            self._update_df_to_be_sorted(self._df, self._df_column_highlights_obj)

        except Exception as exception:
            error_message = f"Data Wrangler can't compute the insights successfully. Use the following error message to help resolve the issue"
            metrics_logger.error(
                create_structured_error_log(
                    exception=exception,
                    event_type=MetricsEventType.LAZY_LOADED.value,
                    message=error_message,
                )
            )
            self._update_error_response(event_type, f"{error_message}: {exception}")

            return EventStatus.FAILED

        else:
            return EventStatus.SUCCESS

    def _log_frontend_version(self, content) -> EventStatus:
        event_type = content["event"]
        frontend_version = content.get("version", "MISSING")

        # parameters validation
        if not is_valid_version(frontend_version):
            metrics_logger.error(
                create_structured_error_log(
                    exception=None,
                    event_type=MetricsEventType.UNEXPECTED_EVENT_PARAMETER.value,
                    message=f"Unexpected event parameter in event {event_type}.",
                )
            )
            return EventStatus.FAILED

        logging.info(f"Installed the frontend version {frontend_version}")

        return EventStatus.SUCCESS

    def _sort_insights(self, content) -> EventStatus:
        try:
            event_type = content["event"]

            column_name = content["data"]["column_name"]

            # parameters validation
            if not is_valid_column_name(column_name, self._df):
                metrics_logger.error(
                    create_structured_error_log(
                        exception=None,
                        event_type=MetricsEventType.UNEXPECTED_EVENT_PARAMETER.value,
                        message=f"Unexpected event parameter in event {event_type}.",
                    )
                )
                return EventStatus.FAILED

            if column_name == "":
                sorted_df = sort_df_rows_by_cell_highlight_count(
                    self._df, self._df_column_highlights_obj
                )
            else:
                sorted_df = sort_df_rows_by_highlight_in_the_column(
                    self._df, self._df_column_highlights_obj, column_name
                )

            self._update_df_and_json(sorted_df)

        except Exception as exception:
            error_message = f"Data Wrangler can't sort the column by data quality issues successfully. Use the following error message to help resolve the issue"
            metrics_logger.error(
                create_structured_error_log(
                    exception=exception,
                    event_type=MetricsEventType.LAZY_LOADED.value,
                    message=error_message,
                )
            )
            self._update_error_response(event_type, f"{error_message}: {exception}")

            return EventStatus.FAILED

        else:
            return EventStatus.SUCCESS
