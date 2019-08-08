from django import forms
Create your models here.
class ConfirmForm(forms.Form):
    options = (
        ("comfort"),
        ("driving"),
        ("interior"),
        ("technology"),
        ("utility")
    )

    # BooleanField
    check_box = forms.MultipleChoiceField(initial=False,
                                          required=False,
                                          widget=forms.CheckboxSelectMultiple,
                                          choices=options)