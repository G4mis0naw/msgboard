import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt

from message.models import messageBoard


def message_board(request):
    message_list = messageBoard.objects.all().order_by('-timestamp')
    return render(request, 'index.html', {'message_list': message_list})


class MessageForm(forms.Form):
    username = forms.CharField(max_length=20)
    content = forms.CharField(max_length=140)


@csrf_exempt
def message_submit(request):
    if request.method == 'POST':
        f = MessageForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            content = f.cleaned_data['content']
        else:
            return message_board(request)

    if content != '':
        save_content = messageBoard()
        save_content.username = username
        save_content.content = content
        save_content.save()
        return HttpResponseRedirect('/message/')
    else:
        return json.dumps({
            'status': 400001,
            'message': "null message",
        })
