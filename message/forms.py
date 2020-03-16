from django import forms


class msgForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, max_length=20)
    content = forms.CharField(widget=forms.TextInput, max_length=140)
