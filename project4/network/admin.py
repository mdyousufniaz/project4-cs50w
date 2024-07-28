from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Post

# Register your models here.

admin.site.register(User)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['writer', 'content', 'creation_time', 'id']