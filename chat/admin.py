from django.contrib import admin
from .models import Contact, Message,UserMessage
# Register your models here.

admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(UserMessage)
