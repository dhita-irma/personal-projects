from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(
        label="Content",
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('title', placeholder='Enter Title', autocomplete='off'),
                Field('body', placeholder='Enter Page Content '),
                Submit('submit', 'Save Entry', css_class='btn btn-primary float-right'), 
                css_class='form-group col-8 offset-2'
            )
        )
