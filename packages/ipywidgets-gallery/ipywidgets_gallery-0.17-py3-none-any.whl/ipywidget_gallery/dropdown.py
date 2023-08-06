import ipywidgets as widgets
from IPython.display import display


class DropdownWithOutput:
    def __init__(self, options, global_var_name):
        self.options = options
        self.global_var_name = global_var_name
        
        # Define the dropdown widget
        self.dropdown = widgets.Dropdown(
            options=options,
            value=options[0],
            description='Select an option:'
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
                print(change.new)

        # Link the dropdown, the global variable, and the output
        self.dropdown.observe(update_global_var, names='value')
        self.dropdown.observe(update_output, names='value')

        # Display the dropdown and the output
        display(self.dropdown)
        display(self.output)
