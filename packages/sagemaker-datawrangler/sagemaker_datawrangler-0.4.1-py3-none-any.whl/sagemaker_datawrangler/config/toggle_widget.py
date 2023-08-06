import logging

import ipywidgets as widgets
import pandas as pd


class ToggleWidget(widgets.VBox):
    """
    Toggle display between the datawrangler widget and the pandas default display
    """

    def __init__(
        self, df, dw_widget_vbox, pandas_default_vbox, displaying_datawrangler=True
    ):
        super().__init__()

        self.dw_widget_vbox = dw_widget_vbox
        # ToDo: optimize by lazy initialization
        self.pandas_default_vbox = pandas_default_vbox

        # ToDo: move to config
        self.displaying_datawrangler = displaying_datawrangler

        self.layout.height = "auto"

        self.render()

    def render(self):
        if self.displaying_datawrangler:
            toggle_button = self._get_to_display_pandas_default_button()
            self.pandas_default_vbox.layout.display = "none"
            self.dw_widget_vbox.layout.display = "block"

            logging.info("Toggled to the sagemaker_datawrangler view.")
        else:
            toggle_button = self._get_to_display_dw_widget_button()
            self.dw_widget_vbox.layout.display = "none"
            self.pandas_default_vbox.layout.display = "block"

            logging.info("Toggled to the pandas default view.")

        self.children = [toggle_button]

    def _get_to_display_dw_widget_button(self):
        button = widgets.Button(description="View Data Wrangler table")
        button.add_class("dw-widget-btn-secondary")

        def _on_button_clicked(button):
            logging.info("Button clicked: View the DataWrangler table")

            self.displaying_datawrangler = True
            self.render()

        button.on_click(_on_button_clicked)
        return button

    def _get_to_display_pandas_default_button(self):
        button = widgets.Button(description="View Pandas table")
        button.add_class("dw-widget-btn-secondary")

        def _on_button_clicked(button):
            logging.info("Button clicked: View the Pandas table")

            self.displaying_datawrangler = False
            self.render()

        button.on_click(_on_button_clicked)
        return button
