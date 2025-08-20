from typing import Final

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.messages import error, success
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from utils import create_activation_account_token, uidb64

from account.forms import LogInForm, RegisterForm
from account.models import ActivationAccountToken, User


def register_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    elif r.method != 'POST':
        return render(r, 'account/register.html', {'form': RegisterForm()})

    form: RegisterForm = RegisterForm(r.POST)

    if not form.is_valid():
        return render(r, 'account/register.html', {'form': form})

    passphrase: str | None = form.cleaned_data.get('passphrase')
    passphrase2: str | None = form.cleaned_data.get('passphrase2')

    if not passphrase or not passphrase2 or passphrase != passphrase2:
        error(r, 'Passphrases does not match.')
        return render(r, 'account/register.html', {'form': form})

    username: str | None = form.cleaned_data.get('username')

    if username is None or User.objects.filter(username=username).exists():
        error(r, 'Username unavailable')
        return render(r, 'account/register.html', {'form': form})

    user: User = User.objects.create_user(  # type: ignore
        username=username,
        password=passphrase,
        is_active=False,
    )

    activate_token: ActivationAccountToken = create_activation_account_token(user)
    uidb64_token: str = uidb64(user.pk)

    success(r, 'Account created. Activate it below.')
    return HttpResponseRedirect(
        reverse('account:activate', args=(uidb64_token, activate_token))
    )


def activate_account_missing_parameter(
    r: HttpRequest, uidb64: str | None = None
) -> HttpResponseRedirect:
    return HttpResponseRedirect(reverse('home:index'))


def activate_account(
    r: HttpRequest, uidb64: str, token: str
) -> HttpResponse | HttpResponseRedirect:
    if r.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    elif r.method != 'POST':
        return render(r, 'account/activate_account.html', {'form': LogInForm()})

    form: Final[LogInForm] = LogInForm(r.POST)

    if not form.is_valid():
        return render(r, 'account/activate_account.html', {'form': form})

    user: User | None = None

    try:
        uuid: str = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uuid, is_active=False)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise Http404()

    token_obj: ActivationAccountToken = get_object_or_404(
        ActivationAccountToken, value=token, used=False
    )

    username: Final[str] = str(form.cleaned_data.get('username'))
    passphrase: Final[str] = str(form.cleaned_data.get('passphrase'))

    user.is_active = True
    user.save()

    if not authenticate(username=username, password=passphrase) == user:
        user.is_active = False
        user.save()

        error(r, 'Invalid username and/or passphrase')
        return render(r, 'account/activate_account.html', {'form': form})

    token_obj.used = True
    token_obj.save()
    login(r, user)

    success(r, 'Account activated successfully!')
    return HttpResponseRedirect(reverse('home:index'))


def login_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    elif r.method != 'POST':
        return render(r, 'account/login.html', {'form': LogInForm()})

    form: Final[LogInForm] = LogInForm(r.POST)

    if not form.is_valid():
        return render(r, 'account/login.html', {'form': form})

    username: Final[str] = str(form.cleaned_data.get('username'))
    passphrase: Final[str] = str(form.cleaned_data.get('passphrase'))

    user: AbstractBaseUser | None = authenticate(username=username, password=passphrase)

    if user is None:
        error(r, 'Invalid username and/or passphrase')
        return render(r, 'account/login.html', {'form': form})

    login(r, user)
    return HttpResponseRedirect(reverse('home:index'))


@login_required(login_url='/account/login')
def logout_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.method == 'POST':
        logout(r)
        return HttpResponseRedirect(reverse('account:login'))

    return render(r, 'account/logout.html')
