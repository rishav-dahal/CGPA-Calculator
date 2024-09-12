from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('name', 'university', 'college', 'avatar')}),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'university', 'college', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'name', 'university', 'college')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Subject)
admin.site.register(Semester)
admin.site.register(UserSubjectGrade)
admin.site.register(AggregateResult)


