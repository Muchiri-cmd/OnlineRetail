from django.contrib import admin
from django.db import models
from userauths.models import User,ContactUs

#Display table
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email']#'bio']



class ContactUsAdmin(admin.ModelAdmin):
    list_display=['full_name','email','subject']

# Register your models here.
admin.site.register(User,UserAdmin)

admin.site.register(ContactUs,ContactUsAdmin)