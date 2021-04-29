from django.contrib import admin
from sign.models import Event,Guest

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'address', 'start_time']

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname','phone','email','sign','create_time','event']


# class EventAdmin(admin.ModelAdmin):
#     list_display = ['id','name','status','address','start_time']
#     #名字搜索
#     search_fields = ['name']
#     #过滤器
#     list_filter = ['status']
#
# class GuestAdmin(admin.ModelAdmin):
#     list_display = ['realname','phone','email','sign','create_time','event']
#     #手机号搜索
#     search_fields = ['realname','phone']
#     #过滤器
#     list_filter = ['sign']

admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)