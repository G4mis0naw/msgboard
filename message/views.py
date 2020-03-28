import json
import uuid

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from message.models import messageBoard, usernameInfo
from django.http import HttpResponse, HttpResponseRedirect

from post.settings import STATICFILES_DIRS


def home(request):
    currentUser = getUser(request)
    message_list = messageBoard.objects.all().order_by('-timestamp')
    return render(request, 'message/index.html', {'message_list': message_list, 'currentUser': currentUser})


# def index(request):
#     return redirect(reverse('message:home'))

def welcome(request):
    return render(request, 'message/welcome.html')


def checkLogin(request):
    ticket = request.COOKIES.get('tickettoken', None)
    if ticket:
        user = usernameInfo.objects.filter(tickettoken=ticket).first()
        if user:
            return user
    return None


def getTicket(request):
    ticket = request.COOKIE.get('tickettoken', None)
    return ticket


def getUser(request):
    user = checkLogin(request)
    if user:
        return user


# 留言板块
def message(request):
    currentUser = getUser(request)
    resp = HttpResponse()
    if request.method == 'POST':
        username = currentUser
        content = request.POST.get('content')
    else:
        return redirect('message:home')

    if content != '':
        if usernameInfo.objects.filter(username=username).exists():
            mess = messageBoard()
            mess.uUsername_id = username
            mess.content = content
            mess.save()
            ret = "Success!"
        else:
            ret = 'User doesn\'t exist!'
    else:
        ret = 'Message invalid!'
    currentUser = getUser(request)
    message_list = messageBoard.objects.all().order_by('-timestamp')
    return render(request, 'message/index.html',
                  {'data': ret, 'message_list': message_list, 'currentUser': currentUser})


# def picUpload(request):


# 用户注册
def register(request):
    if request.method == 'GET':
        return render(request, 'message/signup.html')
    else:
        response = HttpResponse()
        username = request.POST.get('username')
        password = request.POST.get('passwd')

        if username != '':
            if usernameInfo.objects.filter(username=username).exists():
                resp = 'Username already exists!'
            elif password != '':
                save_table = usernameInfo()
                save_table.username = username
                save_table.passwd = password
                try:
                    save_table.save()
                    resp = 'Register success!'
                except BaseException:
                    pass
            else:
                resp = 'password can\'t be empty!'
        else:
            resp = 'Username can\'t be empty!'

        response.content = resp
        return response


# 用户登录
def login(request):
    if request.method == 'GET':
        currentUser = getUser(request)
        if currentUser:
            return redirect('/home')
        else:
            return render(request, 'message/login.html', {'currentUser': currentUser})
    else:
        username = request.POST.get('username')
        password = request.POST.get('passwd')
        response = HttpResponse()
        if usernameInfo.objects.filter(username=username).exists():
            user = usernameInfo.objects.get(username=username)
            if user.passwd == password:
                token = str(uuid.uuid4())
                response.set_cookie('tickettoken', token, expires=9000)
                response.set_cookie('uid', user.id, expires=9000)
                user.tickettoken = token
                try:
                    user.save()
                    resp = 'Login success!'
                except BaseException as e:
                    pass
            else:
                resp = {'stat': '0', 'ret': 'Username or password incorrect!'}
        else:
            resp = 'User doesn\'t exist!'
        response.content = json.dumps(resp)
        return response


# 登出
def logout(request):
    response = HttpResponse()
    response.delete_cookie('tickettoken')
    uid = request.COOKIES.get('uid', None)
    if uid:
        content = cache.set('mine' + uid, None)
    response.content = 'Logout success!'
    return response
