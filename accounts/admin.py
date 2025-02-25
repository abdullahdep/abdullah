from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_child_account')
    list_filter = UserAdmin.list_filter + ('userprofile__is_child_account',)

    def is_child_account(self, obj):
        return obj.userprofile.is_child_account
    is_child_account.boolean = True
    is_child_account.short_description = 'Child Account'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

