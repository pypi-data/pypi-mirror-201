import ipywidgets as widgets
from IPython.display import display


class ColorPickerWithOutput:
    """ColorPickerWithOutput: A widget that displays a color picker and an output widget that displays the selected color in hexadecimal format."""

    def __init__(self, label, message, global_var_name, default="#000000"):
        self.color_picker = widgets.ColorPicker(
            description=label, value=default
        )
        self.output = widgets.Output()
        self.value = default

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change["new"]))
                self.value = change["new"]

        self.color_picker.observe(update_output, names="value")
        display(widgets.VBox([self.color_picker, self.output]))
