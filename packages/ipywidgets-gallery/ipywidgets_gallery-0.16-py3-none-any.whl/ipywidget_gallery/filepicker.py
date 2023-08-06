import ipywidgets as widgets
from IPython.display import display

class FilePickerWithOutput:
    '''FilePickerWithOutput: A widget that displays a file picker and an output widget that displays the selected file path.'''
    def __init__(self, label, message, global_var_name):
        self.file_picker = widgets.FileUpload(description=label)
        self.output = widgets.Output()
        self.global_var_name = global_var_name

        def update_output(change):
            with self.output:
                self.output.clear_output()
                if len(change['new']) > 0:
                    print(message.format(list(change['new'].keys())[0]))
                    global_vars = globals()
                    global_vars[self.global_var_name] = list(change['new'].keys())[0]

        self.file_picker.observe(update_output, names='value')
        display(widgets.VBox([self.file_picker, self.output]))