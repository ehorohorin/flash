from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User
from .models import Problem
from .models import Comment
from .models import Status
from .models import Vote

admin.site.register(User, UserAdmin)
admin.site.register(Problem)
admin.site.register(Comment)
admin.site.register(Status)
admin.site.register(Vote)


