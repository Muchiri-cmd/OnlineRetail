from django.contrib import admin
from userauths.models import User

#Display table
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','bio']

# Register your models here.
admin.site.register(User,UserAdmin)