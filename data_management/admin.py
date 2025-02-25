from django.contrib import admin
from .models import UserData, SharedData

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(SharedData)
class SharedDataAdmin(admin.ModelAdmin):
    list_display = ('parent_data', 'child_account')
    list_filter = ('child_account',)
    search_fields = ('parent_data__title', 'child_account__username')

