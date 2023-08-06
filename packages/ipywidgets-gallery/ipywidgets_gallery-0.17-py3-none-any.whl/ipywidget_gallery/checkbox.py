import ipywidgets as widgets
from IPython.display import display


class CheckboxWithOutput:
    def __init__(self, label, message, global_var_name):
        self.checkbox = widgets.Checkbox(description=label)
        self.output = widgets.Output()
        self.global_var_name = global_var_name

        def update_output(change):
            with self.output:
                self.output.clear_output()
                if change['new']:
                    print(message)
                    global_vars = globals()
                    global_vars[self.global_var_name] = True
                else:
                    global_vars = globals()
                    global_vars[self.global_var_name] = False

        self.checkbox.observe(update_output, names='value')
        display(widgets.VBox([self.checkbox, self.output]))