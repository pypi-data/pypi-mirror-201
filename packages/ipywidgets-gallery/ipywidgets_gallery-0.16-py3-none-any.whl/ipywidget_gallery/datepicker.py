import ipywidgets as widgets
from IPython.display import display


class DatePickerWithOutput:
    '''DatePickerWithOutput: A widget that displays a date picker and an output widget that displays the selected date.'''
    def __init__(self, label, message, global_var_name):
        self.date_picker = widgets.DatePicker(description=label)
        self.output = widgets.Output()
        self.global_var_name = global_var_name

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change['new']))
                global_vars = globals()
                global_vars[self.global_var_name] = str(change['new'])

        self.date_picker.observe(update_output, names='value')
        display(widgets.VBox([self.date_picker, self.output]))