from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from message.forms import msgForm


def index(request):
    return render(request, "index.html")


def get_msg(request):
    if request.method == 'POST':
        msg_form = msgForm(request.POST)
        if msg_form.is_valid():
            username = msg_form.cleaned_data['username']
            content = msg_form.cleaned_data['content']
    return HttpResponseRedirect('/index/')
