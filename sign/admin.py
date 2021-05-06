# from django.contrib import admin
# from sign.models import Event,Guest
#
# # Register your models here.
# class EventAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'status', 'address', 'start_time']
#     #名字搜索
#     search_fields = ['name']
#     #过滤器
#     list_filter = ['status']
#
# class GuestAdmin(admin.ModelAdmin):
#     list_display = ['realname','phone','email','sign','create_time','event']
#     # 手机号搜索
#     search_fields = ['realname', 'phone']
#     # 过滤器
#     list_filter = ['sign']
#
# admin.site.register(Event,EventAdmin)
# admin.site.register(Guest,GuestAdmin)

from django.contrib import admin
from sign.models import *


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_time','id']
    search_fields = ['name']    # 搜索功能
    list_filter = ['status']    # 过滤器


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone','email','sign','create_time','event_id']
    list_display_links = ('realname', 'phone') # 显示链接
    search_fields = ['realname','phone']       # 搜索功能
    list_filter = ['event_id']                 # 过滤器


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)