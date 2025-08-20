from typing import Final, Self

from captcha.fields import CaptchaField
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import (
    CharField,
    Form,
    ModelForm,
    PasswordInput,
    TextInput,
    ValidationError,
)

from account.models import User


# Admin
class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField(label=('Password'))

    class Meta:
        model = User
        fields = (
            'groups',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'password',
            'user_permissions',
            'username',
        )

    def clean_password(self):
        # Retorna o valor original da senha, não o novo que o usuário tentar digitar
        return self.initial['password']


class UserCreationForm(ModelForm):
    password1: Final[CharField] = CharField(label='Password', widget=PasswordInput)
    password2: Final[CharField] = CharField(
        label='Password confirmation', widget=PasswordInput
    )

    class Meta:
        model = User
        fields: Final[tuple[str]] = ('username',)

    def clean_password2(self: Self):
        password1: str | None = self.cleaned_data.get('password1')
        password2: str | None = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self: Self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# Views
class RegisterForm(Form):
    username: Final[CharField] = CharField(
        label='Username',
        min_length=2,
        max_length=20,
        required=True,
        widget=TextInput(
            attrs={
                'id': 'username',
                'placeholder': 'Enter your username',
                'autofocus': 'autofocus',
                'autocomplete': 'off',
            }
        ),
        help_text='Max of 20 chars. Letters, numbers and "@", ".", "+", "-", "_" only.',
    )
    passphrase: Final[CharField] = CharField(
        label='Passphrase',
        required=True,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase',
                'placeholder': 'Enter your passphrase',
                'autocomplete': 'off',
            }
        ),
        help_text='Use a "passphase", sentence '
        'instead of random characters or just password.',
    )
    passphrase2: Final[CharField] = CharField(
        label='',
        required=True,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase-confirm',
                'placeholder': 'Confirm your passphrase',
                'autocomplete': 'off',
            }
        ),
    )
    captcha: Final[CaptchaField] = CaptchaField()


class LogInForm(Form):
    username: Final[CharField] = CharField(
        label='Username',
        min_length=2,
        max_length=32,
        required=True,
        widget=TextInput(
            attrs={
                'id': 'username',
                'placeholder': 'Enter your username',
                'autofocus': 'autofocus',
                'autocomplete': 'off',
            }
        ),
    )
    passphrase: Final[CharField] = CharField(
        label='Passphrase',
        required=True,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase',
                'placeholder': 'Enter your passphrase',
                'autocomplete': 'off',
            }
        ),
    )
