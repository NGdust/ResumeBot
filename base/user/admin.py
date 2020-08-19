from django.contrib import admin
from .models import User, Candidate, Employer

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    fields = ('email', 'password', 'username',)

@admin.register(Candidate)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    fields = ('email', 'password', 'username', 'name', 'secondname', 'address', 'phone', 'url', 'is_verify', 'black_list', 'comments_admin')

@admin.register(Employer)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    fields = ('email', 'password', 'username', 'company', 'category', 'fio', 'address', 'phone', 'url', 'is_verify', 'black_list', 'comments_admin')
