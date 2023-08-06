import ipywidgets as widgets
from IPython.display import display


class RadioButtonsWithOutput:
    """RadioButtonsWithOutput: A widget that displays a group of radio buttons and an output widget that displays a message when a button is selected."""

    def __init__(self, label, options, message):
        self.radio_buttons = widgets.RadioButtons(
            description=label, options=options
        )
        self.output = widgets.Output()
        self.value = None

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change["new"]))
                self.value = change["new"]

        self.radio_buttons.observe(update_output, names="value")
        display(widgets.VBox([self.radio_buttons, self.output]))
