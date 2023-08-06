import ipywidgets as widgets
from IPython.display import display


class CheckboxWithOutput:
    """CheckboxWithOutput: A widget that displays a checkbox option."""

    def __init__(self, label, message, default=False):
        self.checkbox = widgets.Checkbox(description=label, value=default)
        self.output = widgets.Output()
        self.value = default

        def update_output(change):
            with self.output:
                self.output.clear_output()
                if change["new"]:
                    print(message)
                    self.value = change["new"]
                else:
                    self.value = change["new"]

        self.checkbox.observe(update_output, names="value")
        display(widgets.VBox([self.checkbox, self.output]))
