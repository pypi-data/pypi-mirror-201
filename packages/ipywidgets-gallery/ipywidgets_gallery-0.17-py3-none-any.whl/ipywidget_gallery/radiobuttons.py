import ipywidgets as widgets
from IPython.display import display

class RadioButtonsWithOutput:
    '''RadioButtonsWithOutput: A widget that displays a group of radio buttons and an output widget that displays a message when a button is selected.'''
    def __init__(self, label, options, message, global_var_name):
        self.radio_buttons = widgets.RadioButtons(description=label, options=options)
        self.output = widgets.Output()
        self.global_var_name = global_var_name

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change['new']))
                global_vars = globals()
                global_vars[self.global_var_name] = change['new']

        self.radio_buttons.observe(update_output, names='value')
        display(widgets.VBox([self.radio_buttons, self.output]))
