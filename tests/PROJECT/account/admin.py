from django.contrib.admin import ModelAdmin, site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.forms import UserChangeForm, UserCreationForm
from account.models import ActivationAccountToken, User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_active', 'is_staff', 'created')
    search_fields = ('username',)

    readonly_fields = ('created',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Important dates', {'fields': ('last_login', 'created')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            },
        ),
    )

    ordering = ('username',)


class ActivationAccountTokenAdmin(ModelAdmin):
    list_filter = ('user__is_active',)


site.register(User, UserAdmin)
site.register(ActivationAccountToken, ActivationAccountTokenAdmin)
