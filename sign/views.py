from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

def index(request):
    return render(request,"index.html")

#登录动作
def login_action(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin123':
            response =  HttpResponseRedirect('/event_manage/')
            #添加cookie
            response.set_cookie('user',username,360)
            return response
        else:
            return render(request,'index.html',{'error':'username or password error ！'})

#发布会管理
def event_manage(request):
    #读取浏览器cookie
    username = request.COOKIES.get('user')
    return render(request,'event_manage.html',{"user":username})
