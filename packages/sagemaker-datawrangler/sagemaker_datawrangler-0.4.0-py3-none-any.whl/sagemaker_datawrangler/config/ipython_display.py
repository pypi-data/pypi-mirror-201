import logging
import time

import ipywidgets as widgets
import pandas as pd
from IPython.display import display

from sagemaker_datawrangler.logging.logging import get_metrics_logger
from sagemaker_datawrangler.logging.metrics import (
    EventStatus,
    MetricsEventType,
    create_event_metrics,
    create_structured_error_log,
)

from ..datawrangler import DataWranglerWidget
from .compute_scale_checkbox import get_checkbox
from .toggle_widget import ToggleWidget

metrics_logger = get_metrics_logger()


# ToDo: properly only suppress mime type 'application/vnd.jupyter.stderr' in the widget
def _suppress_warnings():
    import warnings

    warnings.filterwarnings("ignore", category=FutureWarning)


def _display_pandas_only(df: pd.DataFrame):
    widget_data = {
        "text/plain": df.__repr__(),
        "text/html": df._repr_html_(),
    }
    display(widget_data, raw=True)


def _display_toggle_views(df: pd.DataFrame):
    dw_widget = DataWranglerWidget(df)
    dw_widget_vbox = widgets.VBox([dw_widget])

    pandas_default_vbox = widgets.Output()

    toggle_widget = ToggleWidget(
        df, dw_widget_vbox, pandas_default_vbox, dw_widget._is_valid_df_json
    )

    compute_scale_checkbox = get_checkbox(dw_widget, df)

    header_row = widgets.HBox(
        [toggle_widget, compute_scale_checkbox], layout=widgets.Layout(height="auto")
    )

    datawrangler_vbox = widgets.VBox([header_row, dw_widget_vbox, pandas_default_vbox])
    _display_custom_widget(df, datawrangler_vbox)

    widget_data = {
        "text/plain": df.__repr__(),
        "text/html": df._repr_html_(),
    }
    with pandas_default_vbox:
        display(widget_data, raw=True)


def _datawrangler_ipython_display(df, *args, **kwargs):
    """
    Displays a pandas.Dataframe with embedded insights for each column.
    param df: pandas.Dataframe
    """
    # ToDo: check_enabled_sagemaker_datawrangler_widget()

    _suppress_warnings()

    start_time = time.time()
    logging.info(
        create_event_metrics(MetricsEventType.INITIALIZATION.value, EventStatus.START)
    )
    try:
        _display_toggle_views(df)
    except Exception as exception:
        metrics_logger.error(
            create_structured_error_log(
                exception=exception,
                event_type=MetricsEventType.INITIALIZATION.value,
                message=f"Widget initialization error: {exception}",
            )
        )

        # Fallback to the default Pandas display
        _display_pandas_only(df)

        latency = time.time() - start_time
        logging.info(
            create_event_metrics(
                MetricsEventType.INITIALIZATION.value,
                EventStatus.FAILED,
                metadata={"latency": latency},
            )
        )
    else:
        latency = time.time() - start_time
        logging.info(
            create_event_metrics(
                MetricsEventType.INITIALIZATION.value,
                EventStatus.SUCCESS,
                metadata={"latency": latency},
            )
        )


def _display_custom_widget(df, custom_widget):
    custom_widget_vbox = widgets.VBox([custom_widget])

    app_widget_data = {"model_id": custom_widget_vbox._model_id}
    widget_data = {
        "text/plain": df.__repr__(),
        "application/vnd.jupyter.widget-view+json": app_widget_data,
    }

    display(widget_data, raw=True)

    return custom_widget_vbox


def extend_pandas_ipython_display():
    """
    Changes all the pandas.Dataframes display to use the sagemaker_datawrangler widget
    """

    pd.DataFrame._ipython_display_ = _datawrangler_ipython_display
