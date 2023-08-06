import ipywidgets as widgets
from IPython.display import display


class DatePickerWithOutput:
    """DatePickerWithOutput: A widget that displays a date picker and an output widget that displays the selected date."""

    def __init__(self, label, message, default=None):
        self.date_picker = widgets.DatePicker(description=label)
        self.output = widgets.Output()
        self.value = default

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change["new"]))
                self.value = str(change["new"])

        self.date_picker.observe(update_output, names="value")
        display(widgets.VBox([self.date_picker, self.output]))
