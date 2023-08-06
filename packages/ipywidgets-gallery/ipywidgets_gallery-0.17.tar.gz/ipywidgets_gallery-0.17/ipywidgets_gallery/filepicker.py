import ipywidgets as widgets
from IPython.display import display


class FilePickerWithOutput:
    """FilePickerWithOutput: A widget that displays a file picker and an output widget that displays the selected file path."""

    def __init__(self, label, message='Selected file: "{}"'):
        self.file_picker = widgets.FileUpload(description=label)
        self.output = widgets.Output()
        self.value = None

        def update_output(change):
            with self.output:
                self.output.clear_output()
                if len(change["new"]) > 0:
                    print(change["new"])
                    self.value = change["new"]
                    print(message.format(str(self.value)))

        self.file_picker.observe(update_output, names="value")
        display(widgets.VBox([self.file_picker, self.output]))
