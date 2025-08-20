from typing import cast

from django.contrib.auth import get_user
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import ActivationAccountToken, User


class BaseAccountTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            password='passphrase',
            is_active=True,
        )

        self.REGISTER_URL: str = reverse('account:register')
        self.LOGIN_URL: str = reverse('account:login')
        self.LOGOUT_URL: str = reverse('account:logout')


class RegisterViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /account/register | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.REGISTER_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_invalid_form(self) -> None:
        """POST /account/register | anonymous user | invalid form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            self.REGISTER_URL, {'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_different_passphrases(self) -> None:
        """POST /account/register | anonymous user | different passphrases"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str] = {
            'username': 'username',
            'email': 'another@example.com',
            'passphrase': '12345678',
            'passphrase2': '11223344',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_existing_register(self) -> None:
        """POST /account/register | anonymous user | register already exists"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str] = {
            'username': 'user',
            'email': 'email@example.com',
            'passphrase': 'passphrase',
            'passphrase2': 'passphrase',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_names(self) -> None:
        """POST /account/register | anonymous user | empty username"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str | None] = {
            'username': '',
            'email': 'email@example.com',
            'passphrase': 'passphrase',
            'passphrase2': 'passphrase',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_valid_form(self) -> None:
        """POST /account/register | anonymous user | valid form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str] = {
            'username': 'username',
            'email': 'another@example.com',
            'passphrase': 'passphrase',
            'passphrase2': 'passphrase',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/activate_account.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /account/register | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='passphrase'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.REGISTER_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(self.REGISTER_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')


class ActivateAccountViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user_no_parameter(self) -> None:
        """GET /account/activate/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('account:activate_no_parameter'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_parameter'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_missing_token(self) -> None:
        """GET /account/activate/<Any> | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_token', args=['404'])
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_token', args=['404']), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_invalid_uidb64(self) -> None:
        """GET /account/activate/<uidb64>/<token> | anonymous user | invalid uidb64"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=['404', 'x' * 64])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/activate_account.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_inexistent_token(self) -> None:
        """GET /account/activate/<uidb64>/<token> | anonymous user | inexistent token"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        user: User = cast(User, User.objects.first())
        user_pk: str = user.pk
        uidb64_pk = urlsafe_base64_encode(force_bytes(user_pk))

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, 'x' * 64])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/activate_account.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user(self) -> None:
        """GET /account/activate/<uidb64>/<token> | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        user: User = cast(User, User.objects.first())

        uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value]), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/activate_account.html')
        # Logged user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /account/activate/<uidb64>/<token> | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='passphrase'))

        user: User = cast(User, User.objects.first())

        uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value]), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class LoginViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /account/login | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {
                'username': 'user',
                'passphrase': 'passphrase',
                'email': 'email@example.com',
            },
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_invalid_form(self) -> None:
        """GET /account/login | anonymous user | invalid form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {'username': 'user', 'email': 'email@example.com'},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_user_is_None(self) -> None:
        """GET /account/login | anonymous user | user is None"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {
                'username': 'fake_user',
                'passphrase': 'passphrase',
                'email': 'email@example.com',
            },
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /account/login | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='passphrase'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(self.LOGIN_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')


class LogoutViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /account/logout | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGOUT_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.LOGIN_URL + '?next=' + self.LOGOUT_URL)

        res: HttpResponse = self.client.get(self.LOGOUT_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /account/logout | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='passphrase'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGOUT_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/logout.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user(self) -> None:
        """POST /account/logout | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='passphrase'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(self.LOGOUT_URL)

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertEqual(res.status_code, 302)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='passphrase'))

        res: HttpResponse = self.client.post(self.LOGOUT_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
