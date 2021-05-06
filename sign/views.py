from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
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

#发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user',"")
    search_name = request.GET.get('name',"")
    event_list = Event.objects.filter(name__contains=search_name)
    return render((request,"event_manage.html",{"user":username,"events":event_list}))

#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user',"")
    guest_list = Guest.objects.all()
    #每页显示2条数据
    paginator = Paginator(guest_list,2)
    #通过get请求得到当前要显示第几页的数据
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        #如果page不是整数，取第一页面数据
        contacts = paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":guest_list})

#嘉宾搜索
@login_required
def search_name(request):
    username = request.session.get('user',"")
    search_name = request.GET.get('name',"")
    guest_list = Guest.objects.filter(name__contains=search_name)
    return render((request,"guest_manage",{"user":username,"events":guest_list}))