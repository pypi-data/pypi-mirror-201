import ipywidgets as widgets
from IPython.display import display


class SelectMultipleWithOutput:
    """SelectMultipleWithOutput: A widget that displays a list of options and an output widget that displays the selected options when they are changed."""

    def __init__(self, label, options, message):
        self.select_multiple = widgets.SelectMultiple(
            description=label, options=options
        )
        self.output = widgets.Output()
        self.value = None

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change["new"]))
                self.value = change["new"]

        self.select_multiple.observe(update_output, names="value")
        display(widgets.VBox([self.select_multiple, self.output]))
