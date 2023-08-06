import ipywidgets as widgets
from IPython.display import display


class ToggleButtonWithOutput:
    # ToggleButtonWithOutput: A widget that displays a toggle button and an output widget that displays a message when the button is toggled.

    def __init__(self, label, message="Toggle Button value: {}"):
        self.button = widgets.ToggleButton(description=label)
        self.output = widgets.Output()
        self.value = None

        def update_output(change):
            with self.output:
                self.output.clear_output()
                if change["new"]:
                    print(message.format(str(change["new"])))
                    self.value = change["new"]
                else:
                    self.value = change["new"]

        self.button.observe(update_output, "value")
        display(widgets.VBox([self.button, self.output]))
