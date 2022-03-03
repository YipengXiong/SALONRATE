from csv import list_dialects
from django.contrib import admin

from salonrate.models import Salon, Service, Comment, Follows


# Register your models here.
class SalonAdmin(admin.ModelAdmin):
    list_display = ('salon_id', 'salon_name', 'salon_address', 'salon_rate', 'salon_busy')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'salon_id', 'service_name', 'service_type', 'service_price', 'service_rate')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'user_id', 'salon_or_service_id', 'comment')

class FollowsAdmin(admin.ModelAdmin):
    list_dispaly = ('user_id', 'salon_id')

admin.site.register(Salon, SalonAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follows, FollowsAdmin)
