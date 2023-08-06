import ipywidgets as widgets
from IPython.display import display

class TextAreaWithOutput:
    '''TextAreaWithOutput: A widget that displays a text area and an output widget that displays the contents of the text area when it is changed.'''
    def __init__(self, label, message, global_var_name):
        self.text_area = widgets.Textarea(description=label)
        self.output = widgets.Output()
        self.global_var_name = global_var_name

        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(message.format(change['new']))
                global_vars = globals()
                global_vars[self.global_var_name] = change['new']

        self.text_area.observe(update_output, names='value')
        display(widgets.VBox([self.text_area, self.output]))