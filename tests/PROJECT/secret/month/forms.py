from django import forms

from .widgets import MonthSelectorWidget


class MonthField(forms.DateField):
    widget = MonthSelectorWidget
