# from django.shortcuts import render,get_object_or_404
# from django.http import HttpResponse,HttpResponseRedirect
# from django.contrib import auth
# from django.contrib.auth.decorators import login_required
# from sign.models import Event,Guest
# from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
#
# # Create your views here.
#
# def index(request):
#     return render(request,"index.html")
#
# #登录动作
# def login_action(request):
#     if request.method=='POST':
#         username = request.POST.get('username','')
#         password = request.POST.get('password','')
#         user = auth.authenticate(username = username,password = password)
#         if user is not None:
#             #登录
#             auth.login(request,user)
#             #将session信息记录到浏览器
#             request.session['user'] = username
#             response = HttpResponseRedirect('/event_manage/')
#             return response
#         else:
#             return render(request,'index.html',{'error':'username or password error ！'})
#
# #发布会管理
# @login_required
# def event_manage(request):
#     #读取浏览器cookie
#     #username = request.COOKIES.get('user')
#
#     event_list = Event.objects.all()
#     #读取浏览器session
#     username = request.session.get('user')
#     return render(request,'event_manage.html',{"user":username,"events":event_list})
#
# #发布会名称搜索
# @login_required
# def search_name(request):
#     username = request.session.get('user',"")
#     search_name = request.GET.get('name',"")
#     event_list = Event.objects.filter(name__contains=search_name)
#     return render((request,"event_manage.html",{"user":username,"events":event_list}))
#
# #嘉宾管理
# @login_required
# def guest_manage(request):
#     username = request.session.get('user',"")
#     guest_list = Guest.objects.all()
#     #每页显示2条数据
#     paginator = Paginator(guest_list,2)
#     #通过get请求得到当前要显示第几页的数据
#     page = request.GET.get('page')
#     try:
#         contacts = paginator.page(page)
#     except PageNotAnInteger:
#         #如果page不是整数，取第一页面数据
#         contacts = paginator.page(paginator.num_pages)
#     return render(request,"guest_manage.html",{"user":username,"guests":guest_list})
#
# #嘉宾搜索
# @login_required
# def search_name(request):
#     username = request.session.get('user',"")
#     search_name = request.GET.get('name',"")
#     guest_list = Guest.objects.filter(name__contains=search_name)
#     return render((request,"guest_manage",{"user":username,"events":guest_list}))
#
# #签到页面
# @login_required
# def sign_index(request,eid):
#     #get_object_or_404 如果对象不存在则抛出http404异常
#     event = get_object_or_404(Event,id = eid)
#     return render(request,'sign_index.html',{'event':event})
#
# #签到动作
# @login_required
# def sign_index_action(request,eid):
#     event = get_object_or_404(Event,id = eid)
#     phone = request.POST.get("phone","")
#     print(phone)
#     #验证手机号在guest表内是否存在
#     result = Guest.objects.filter(phone = phone)
#     #不存在则提示phone error.
#     if not result:
#         return render(request,"sign_index.html",{"event":event,"hint":'phone error.'})
#
#     #通过手机号和发布会id来查询guest表
#     result = Guest.objects.filter(phone = phone,event_id=eid)
#     #如果不匹配，则提示 event id or phone error
#     if not result:
#         return render(request,'sign_index.html',{"event":event,"hint":'event id or phone error.'})
#
#     result = Guest.objects.filter(phone = phone,event_id=eid)
#     #如果不匹配，则提示用户已经签到过
#     if not result:
#         return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.'})
#
#     #否则就进行签到动作，修改sign=1，提示用户签到成功
#     else:
#         Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
#         return render(request,'sign_index.html',{'event':event,
#                                                  'hint':'sign in success!',
#                                                  'guest':result})
#
# #退出登录
# @login_required
# def logout(request):
#     #退出登录
#     auth.logout(request)
#     response = HttpResponseRedirect('/index/')
#     return response
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Event,Guest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

logger = logging.getLogger(__name__)


# Create your views here.
# 首页(登录)
def index(request):
    return render(request,"index.html")


# 登录动作
def login_action(request):
    if request.method == "POST":
        # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        if username == '' or password == '':
            return render(request,"index.html",{"error":"username or password null!"})

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user) # 验证登录
            response = HttpResponseRedirect('/event_manage/') # 登录成功跳转发布会管理
            request.session['username'] = username    # 将 session 信息写到服务器
            return response
        else:
            return render(request,"index.html",{"error":"username or password error!"})
    # 防止直接通过浏览器访问 /login_action/ 地址。
    return render(request,"index.html")

# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response


# 发布会管理（登录之后默认页面）
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('username', '')
    return render(request, "event_manage.html", {"user": username,"events":event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    search_name_bytes = search_name.encode(encoding="utf-8")
    event_list = Event.objects.filter(name__contains=search_name_bytes)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username,
                                                   "guests": contacts,
                                                   "phone":search_phone})


# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)           # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)   # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,
                                               'guest':guest_data,
                                               'sign':sign_data})


# 前端签到页面
def sign_index2(request,event_id):
    event_name = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index2.html',{'eventId': event_id,
                                               'eventNanme': event_name})


# 签到动作
@login_required
def sign_index_action(request,event_id):

    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    guest_data = str(len(guest_list))
    sign_data = 0   #计算发布会“已签到”的数量
    for guest in guest_list:
        if guest.sign == True:
            sign_data += 1

    phone =  request.POST.get('phone','')

    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.filter(phone = phone,event_id = event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})

    result = Guest.objects.get(event_id = event_id,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
    else:
        Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
            'user': result,
            'guest':guest_data,
            'sign':str(int(sign_data)+1)
            })
