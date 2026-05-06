from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Subscription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name',
        'last_name', 'is_staff', 'is_active'
    )
    list_display_links = ('id', 'email', 'username')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ('-id',)
    personal_info_fields = ('first_name', 'last_name', 'avatar')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'avatar')},
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {'fields': ('last_login', 'date_joined')},
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name',
                'password1', 'password2',
            ),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'created_at')
    list_display_links = ('id', 'user', 'author')
    search_fields = (
        'user__username', 'user__email', 'author__username', 'author__email'
    )
    list_filter = ('created_at',)
    ordering = ('-created_at',)
