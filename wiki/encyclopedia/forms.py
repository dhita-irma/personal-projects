from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="Title", 
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Title', 
            'autocomplete': 'off'
            }))
    body = forms.CharField(
        label="Content", 
        widget=forms.Textarea(attrs={'placeholder': 'Enter Page Content'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-8 offset-2')
                ),
            Row(
                Column('body', css_class='form-group col-8 offset-2')
            ),
            Row(
                Column(Submit('submit', 'Create Entry', css_class='btn btn-primary float-right'),
                css_class='form-group col-8 offset-2')
            )
        )