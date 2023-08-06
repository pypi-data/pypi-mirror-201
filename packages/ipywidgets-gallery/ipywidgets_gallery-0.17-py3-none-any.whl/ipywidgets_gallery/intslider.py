import ipywidgets as widgets
from IPython.display import display


class IntSliderWithOutput:
    """IntSliderWithOutput: A widget that displays an integer slider and an output widget that displays the current value of the slider."""

    def __init__(
        self,
        label,
        min_value,
        max_value,
        message,
        default=None,
    ):
        self.slider = widgets.IntSlider(
            description=label, min=min_value, max=max_value
        )
        self.output = widgets.Output()
        self.value = default or min_value

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change["new"]))
                self.value = change["new"]

        self.slider.observe(update_output, names="value")
        display(widgets.VBox([self.slider, self.output]))
