import ipywidgets as widgets
from IPython.display import display


class ToggleButtonGroupWithOutput:
    '''ToggleButtonWithOutput: A widget that displays a toggle button and an output widget that displays a message when the button is toggled.'''
    def __init__(self, label, options, message, global_var_name):
        self.toggle_buttons = widgets.ToggleButtons(description=label, options=options)
        self.output = widgets.Output()
        self.global_var_name = global_var_name

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change['new']))
                global_vars = globals()
                global_vars[self.global_var_name] = change['new']

        self.toggle_buttons.observe(update_output, names='value')
        display(widgets.VBox([self.toggle_buttons, self.output]))
