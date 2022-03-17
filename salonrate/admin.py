from csv import list_dialects
import site
from django.contrib import admin

from salonrate.models import Salon, Service, Comment, Follows, UserProfile
from salonrate.views import register


# Register your models here.
class SalonAdmin(admin.ModelAdmin):
    list_display = ('salon_id', 'salon_name', 'salon_address', 'rate', 'salon_busy')
    prepopulated_fields = {'slug':('salon_name',)}

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'salon_id', 'service_name', 'service_type', 'service_price', 'rate')
    prepopulated_fields = {'slug':('service_name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'username', 'salon_or_service_id', 'comment')

class FollowsAdmin(admin.ModelAdmin):
    list_dispaly = ('username', 'salon_id')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

admin.site.register(Salon, SalonAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follows, FollowsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
