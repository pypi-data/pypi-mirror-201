import ipywidgets as widgets
from IPython.display import display


class DropdownWithOutput:
    """DropdownWithOutput: A widget that displays a dropdown menu and an output widget that displays the selected option."""

    def __init__(self, options, default=None):
        self.options = options
        self.value = default or options[0]

        # Define the dropdown widget
        self.dropdown = widgets.Dropdown(
            options=options, value=options[0], description="Select an option:"
        )

        # Define the output widget
        self.output = widgets.Output()

        # Define the function to update the output widget
        def update_output(change):
            with self.output:
                self.output.clear_output()
                print(change.new)
                self.value = change.new

        # Link the dropdown, the global variable, and the output
        self.dropdown.observe(update_output, names="value")

        # Display the dropdown and the output
        display(self.dropdown)
        display(self.output)
