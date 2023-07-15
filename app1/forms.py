from django import forms

class TextareaForm(forms.Form):
    my_textarea_field = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))
