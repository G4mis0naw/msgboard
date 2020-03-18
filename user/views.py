import json
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from user.models import usernameInfo


def signup_box(request):
    return render(request, 'signup.html')


class signupForm(forms.Form):
    username = forms.CharField(max_length=20)
    passwd = forms.CharField(max_length=140)


def register(request):
    n = signupForm(request.POST)
    if request.method == 'POST':
        if n.is_valid():
            username = n.cleaned_data['username']
            passwd = n.cleaned_data['passwd']
        else:
            return signup_box(request)

    if username != '':
        save_table = usernameInfo()
        save_table.username = username
        save_table.passwd = passwd
        save_table.save()
        return HttpResponseRedirect('/')
    else:
        return json.dumps({
            'status': 400001,
            'message': "invalid signup",
        })