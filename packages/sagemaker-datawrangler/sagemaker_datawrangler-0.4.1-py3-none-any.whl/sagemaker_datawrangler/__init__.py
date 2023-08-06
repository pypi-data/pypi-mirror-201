# Copyright 2022 Amazon.com (http://amazon.com/), Inc. or its affiliates. All Rights Reserved.This is AWS Content subject to the terms of the Customer Agreement


#!/usr/bin/env python
# coding: utf-8
import logging

from ._version import __version__, version_info
from .logging.logging import get_metrics_logger, setup_logging
from .logging.metrics import create_session_start_log

"""
Override the pandas.DataFrame._ipython_display_ method to register the DataWrangler widget display 
"""
from .config.ipython_display import extend_pandas_ipython_display

try:
    setup_logging()
    metrics_logger = get_metrics_logger()
except Exception as exception:
    logging.exception(f"Error while setting up logging {exception}")

metrics_logger.info(create_session_start_log())
extend_pandas_ipython_display()


def _jupyter_labextension_paths():
    """Called by Jupyter Lab Server to detect if it is a valid labextension and
    to install the widget
    Returns
    =======
    src: Source directory name to copy files from. Webpack outputs generated files
        into this directory and Jupyter Lab copies from this directory during
        widget installation
    dest: Destination directory name to install widget files to. Jupyter Lab copies
        from `src` directory into <jupyter path>/labextensions/<dest> directory
        during widget installation
    """
    return [
        {
            "src": "labextension",
            "dest": "sagemaker_datawrangler",
        }
    ]


def _jupyter_nbextension_paths():
    """Called by Jupyter Notebook Server to detect if it is a valid nbextension and
    to install the widget
    Returns
    =======
    section: The section of the Jupyter Notebook Server to change.
        Must be 'notebook' for widget extensions
    src: Source directory name to copy files from. Webpack outputs generated files
        into this directory and Jupyter Notebook copies from this directory during
        widget installation
    dest: Destination directory name to install widget files to. Jupyter Notebook copies
        from `src` directory into <jupyter path>/nbextensions/<dest> directory
        during widget installation
    require: Path to importable AMD Javascript module inside the
        <jupyter path>/nbextensions/<dest> directory
    """
    return [
        {
            "section": "notebook",
            "src": "nbextension",
            "dest": "sagemaker_datawrangler",
            "require": "sagemaker_datawrangler/extension",
        }
    ]
