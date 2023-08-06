# test_ipywidgets_gallery.py

from ipywidgets_gallery import (
    CheckboxWithOutput,
    ColorPickerWithOutput,
    DatePickerWithOutput,
    DropdownWithOutput,
    RadioButtonsWithOutput,
    SelectMultipleWithOutput,
    TextAreaWithOutput,
    ToggleButtonWithOutput,
)

import ipywidgets as widgets


def test_checkbox_output():
    checkbox = CheckboxWithOutput("Label", "Checkbox is {}", True)
    assert isinstance(checkbox.checkbox, widgets.Checkbox)
    assert checkbox.value == True


def test_colorpicker_output():
    colorpicker = ColorPickerWithOutput("Label", "Color is {}", "#FFFFFF")
    assert isinstance(colorpicker.color_picker, widgets.ColorPicker)


def test_datepicker_output():
    datepicker = DatePickerWithOutput("Label", "Date is {}", "11/30/1986")
    assert isinstance(datepicker.date_picker, widgets.DatePicker)


def test_dropdown_output():
    dropdown = DropdownWithOutput(["a", "b", "c"], "a")
    assert isinstance(dropdown.dropdown, widgets.Dropdown)
