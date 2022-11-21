from django.contrib import admin
from account_app.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','First_name', 'Last_name','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('UserCredentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('First_name', 'Last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password', 'password2' 'First_name','Last_name')
        }),
    )
    search_fields = ('email','First_name','Last_name',)
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)

# admin.site.register(User, UserModelAdmin)

# class AdminUserPermissionMixin:
#     def has_view_permission(self, request, obj=None):
#         return request.user.is_admin

#     def has_add_permission(self, request):
#         return False