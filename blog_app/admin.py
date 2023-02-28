from django.contrib import admin
from .models import UserAccount,Post,OTPStorage,Comment,Following,Reply

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Post)
admin.site.register(OTPStorage)
admin.site.register(Comment)
admin.site.register(Following)
admin.site.register(Reply)

# admin.site.register(Followers)

