import json
import random
import time
from django.shortcuts import render
from message.models import messageBoard, usernameInfo
from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect


def message_board(request):
    message_list = messageBoard.objects.all().order_by('-timestamp')
    return render(request, 'message/index.html', {'message_list': message_list})


def signup_box(request):
    return render(request, 'message/signup.html')


def login_box(request):
    return render(request, 'message/login.html')


class MessageForm(forms.Form):
    username = forms.CharField(max_length=20)
    content = forms.CharField(max_length=140)


def message_submit(request):
    f = MessageForm(request.POST)
    if request.method == 'POST':
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
        return HttpResponseRedirect('/')
    else:
        return json.dumps({
            'status': 400001,
            'message': "null message",
        })


class signupForm(forms.Form):
    username = forms.CharField(max_length=20)
    passwd = forms.CharField(max_length=140)


class loginForm(forms.Form):
    username = forms.CharField(max_length=20)
    passwd = forms.CharField(max_length=140)


def register(request):
    n = signupForm(request.POST)
    if request.method == 'GET':
        return render(request, 'message/signup.html', {'error': 'What do you want？'})  # 尝试返回弹窗
    if request.method == 'POST':
        if n.is_valid():
            username = n.cleaned_data['username']
            passwd = n.cleaned_data['passwd']
            passwd = make_password(passwd)
        else:
            return signup_box(request)

    if username != '':
        save_table = usernameInfo()
        save_table.username = username
        save_table.passwd = passwd
        save_table.save()
        return HttpResponseRedirect('index')
    else:
        return json.dumps({
            'status': 400001,
            'message': "invalid signup",
        })


def login(request):
    l = loginForm(request.POST)
    if request.method == 'GET':
        return render(request, 'login/', {'error': 'What do u want？'})
    elif request.method == 'POST':
        if l.is_valid():
            username = l.cleaned_data['username']
            passwd = l.cleaned_data['passwd']
            if usernameInfo.objects.filter(username=username).exists():
                user = usernameInfo.objects.get(username=username)
                if check_password(passwd, user.passwd):
                    ticket = ''
                    for i in range(12):
                        s = 'abcdefghijklmnopqrstuvwxyz'
                        ticket += random.choice(s)
                    now_time = int(time.time())
                    ticket = 'TK' + ticket + str(now_time)
                    response = HttpResponseRedirect('index.html')
                    response.set_cookie('ticket', ticket, max_age=10000)
                    user.ticket = ticket
                    user.save()
                    return response
                else:
                    return render(request, 'index', {'password': 'Wrong password'})
            else:
                return render(request, 'login/', {'name': 'User doesn\'t exists，signup first'})
    else:
        return login_box(request)
