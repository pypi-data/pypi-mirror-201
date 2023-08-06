import ipywidgets as widgets
from IPython.display import display


class RangeSliderWithOutput:
    '''RangeSliderWithOutput: A widget that displays an float slider and an output widget that displays the current value of the slider.'''
    def __init__(self, min_val, max_val, step, global_var_name):
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.global_var_name = global_var_name

        # Define the RangeSlider widget
        self.slider = widgets.FloatRangeSlider(
            value=[min_val, max_val],
            min=min_val,
            max=max_val,
            step=step,
            description='Range:'
        )

        # Define the output widget
        self.output = widgets.Output()

        # Define the function to update the global variable
        def update_global_var(change):
            global_vars = globals()
            global_vars[self.global_var_name] = change.new

        # Define the function to update the output widget
        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(f"Selected range: {change.new[0]:.2f} - {change.new[1]:.2f}")

        # Link the slider, the global variable, and the output
        self.slider.observe(update_global_var, names='value')
        self.slider.observe(update_output, names='value')

        # Display the slider and the output
        display(widgets.HBox([self.slider, self.output]))
