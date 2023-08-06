import ipywidgets as widgets
from IPython.display import display

class ColorPickerWithOutput:
    '''ColorPickerWithOutput: A widget that displays a color picker and an output widget that displays the selected color in hexadecimal format.'''
    def __init__(self, label, message, global_var_name):
        self.color_picker = widgets.ColorPicker(description=label)
        self.output = widgets.Output()
        self.global_var_name = global_var_name

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change['new']))
                global_vars = globals()
                global_vars[self.global_var_name] = change['new']

        self.color_picker.observe(update_output, names='value')
        display(widgets.VBox([self.color_picker, self.output]))
