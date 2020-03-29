import uuid

from django.core.cache import cache
from django.shortcuts import render, redirect
from ratelimit.decorators import ratelimit

from message.models import messageBoard, usernameInfo
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    currentUser = getUser(request)
    message_list = messageBoard.objects.all().order_by('-timestamp')
    return render(request, 'message/index.html', {'message_list': message_list, 'currentUser': currentUser})


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
@ratelimit(key='post:ip', rate='5/m', block=True)
def message(request):
    currentUser = getUser(request)
    resp = HttpResponse()
    if request.method == 'POST':
        username = currentUser
        content = request.POST.get('content')
        uimage = request.FILES.get('image')
    else:
        return redirect('message:home')

    if content != '' and content != '\n':
        if usernameInfo.objects.filter(username=username).exists():
            mess = messageBoard()
            mess.uUsername_id = username
            mess.content = content
            mess.image = uimage
            mess.save()
            ret = "留言成功！"
        else:
            ret = '用户不存在！'
    else:
        ret = '消息不能为空！'
    currentUser = getUser(request)
    message_list = messageBoard.objects.all().order_by('-timestamp')
    return render(request, 'message/index.html',
                  {'data': ret, 'message_list': message_list, 'currentUser': currentUser})


# 用户注册
def register(request):
    if request.method == 'GET':
        return render(request, 'message/signup.html')
        if currentUser:
            return redirect('/home')
        else:
            return render(request, 'message/login.html', {'currentUser': currentUser})
    else:
        username = request.POST.get('username')
        password = request.POST.get('passwd')

        if username != '':
            if usernameInfo.objects.filter(username=username).exists():
                resp = '用户已经存在，请直接登录'
            elif password != '':
                save_table = usernameInfo()
                save_table.username = username
                save_table.passwd = password
                try:
                    save_table.save()
                    response = HttpResponseRedirect('/login')
                    return response
                except BaseException:
                    pass
            else:
                resp = '密码不能为空'
        else:
            resp = '用户名不能为空'
        return render(request, 'message/signup.html', {'resp': resp})


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
        if usernameInfo.objects.filter(username=username).exists():
            user = usernameInfo.objects.get(username=username)
            if user.passwd == password:
                token = str(uuid.uuid4())
                response = HttpResponseRedirect('/home')
                response.set_cookie('tickettoken', token, expires=9000)
                response.set_cookie('uid', user.id, expires=9000)
                user.tickettoken = token
                try:
                    user.save()
                    return response
                except BaseException as e:
                    pass
                    resp = '登录失败，检查输入信息！'
            else:
                resp = '用户名或密码错误'
        else:
            resp = '用户不存在！请先注册'
        return render(request, 'message/login.html', {'resp': resp})


# 登出
def logout(request):
    response = HttpResponseRedirect('/home')
    response.delete_cookie('tickettoken')
    uid = request.COOKIES.get('uid', None)
    if uid:
        content = cache.set('mine' + uid, None)
    return response


def page_not_found(request):
    return render(request, '404.html')


def delete(request, id):
    msg = messageBoard.objects.get(id=id)
    currentUser = getUser(request)
    if msg.uUsername == currentUser:
        try:
            msg.delete()
            return redirect('message:home')
        except BaseException:
            pass
    else:
        return redirect('message:home')