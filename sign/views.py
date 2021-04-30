from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event
# Create your views here.

def index(request):
    return render(request,"index.html")

#登录动作
def login_action(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            #登录
            auth.login(request,user)
            #将session信息记录到浏览器
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request,'index.html',{'error':'username or password error ！'})

#发布会管理
@login_required
def event_manage(request):
    #读取浏览器cookie
    #username = request.COOKIES.get('user')

    event_list = Event.objects.all()
    #读取浏览器session
    username = request.session.get('user')
    return render(request,'event_manage.html',{"user":username,"events":event_list})
