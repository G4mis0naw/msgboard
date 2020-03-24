import json
import uuid

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from message.models import messageBoard, usernameInfo
from django.http import HttpResponse


# 留言板页并获得当前用户名
def home(request):
    message_list = messageBoard.objects.all().order_by('-timestamp')
    currentUser = getUser(request)
    return render(request, 'message/index.html', {'message_list': message_list, 'currentUser': currentUser})


# def index(request):
#     return redirect(reverse('message:home'))


def checkLogin(request):
    ticket = request.COOKIES.get('tickettoken', None)
    if ticket:
        user = usernameInfo.objects.filter(tickettoken=ticket).first()
        if user:
            return user
    return None


def getUser(request):
    user = checkLogin(request)
    if user:
        return user


def message(request):
    currentUser = getUser(request)
    if request.method == 'POST':
        username = currentUser
        content = request.POST.get('content')
    else:
        return home(request)

    if content != '':
        save_content = messageBoard()
        save_content.username = username
        save_content.content = content
        save_content.save()
        return redirect('/home/')
    else:
        return json.dumps({
            'status': 400001,
            'message': "null message",
        })


# 用户注册
def register(request):
    if request.method == 'GET':
        return render(request, 'message/signup.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('passwd')

    if username != '':
        save_table = usernameInfo()
        save_table.username = username
        save_table.passwd = password
        save_table.save()
        return render(request, 'message/hello.html')
    else:
        return json.dumps({
            'status': 400001,
            'message': "invalid signup",
        })


# 用户登录
def login(request):
    if request.method == 'GET':
        return render(request, 'message/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('passwd')
        if usernameInfo.objects.filter(username=username).exists():
            user = usernameInfo.objects.get(username=username)
            if user.passwd == password:
                token = str(uuid.uuid4())
                response = HttpResponse()
                response.set_cookie('tickettoken', token, expires=30)
                response.set_cookie('uid', user.id, expires=60)
                user.tickettoken = token
                user.save()
        return response


# 登出
def logout(request):
    response = HttpResponse()
    response.delete_cookie('tickettoken')
    uid = request.COOKIES.get('uid')
    uid = request.COOKIES.get('uid', None)
    if uid:
        content = cache.set('mine' + uid, None)

    response.content = json.dump({'status': '1'})

    return response
