from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404
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

#签到页面
@login_required
def sign_index(request,eid):
    #get_object_or_404 如果对象不存在则抛出http404异常
    event = get_object_or_404(Event,id = eid)
    return render(request,'sign_index.html',{'event':event})

#签到动作
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id = eid)
    phone = request.POST.get("phone","")
    print(phone)
    #验证手机号在guest表内是否存在
    result = Guest.objects.filter(phone = phone)
    #不存在则提示phone error.
    if not result:
        return render(request,"sign_index.html",{"event":event,"hint":'phone error.'})

    #通过手机号和发布会id来查询guest表
    result = Guest.objects.filter(phone = phone,event_id=eid)
    #如果不匹配，则提示 event id or phone error
    if not result:
        return render(request,'sign_index.html',{"event":event,"hint":'event id or phone error.'})

    result = Guest.objects.filter(phone = phone,event_id=eid)
    #如果不匹配，则提示用户已经签到过
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.'})

    #否则就进行签到动作，修改sign=1，提示用户签到成功
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign_index.html',{'event':event,
                                                 'hint':'sign in success!',
                                                 'guest':result})