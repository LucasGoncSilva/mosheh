from account.models import User
from django.contrib.auth import get_user
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from secret.models import LoginCredential, PaymentCard, SecurityNote
from secret.month.models import Month


class HomeViewsTestCase(TestCase):
    def setUp(self) -> None:
        user: User = User.objects.create_user(
            username='user',
            password='passphrase',
            is_active=True,
        )

        PaymentCard.objects.create(
            owner=user,
            name='Personal Main Card',
            card_type='deb',
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank='nubank--',
            brand='mastercard--',
            slug='nubank--personal-main-card',
            owners_name='TEST USER',
        )

        LoginCredential.objects.create(
            owner=user,
            service='google--',
            name='Personal Main Account',
            slug='google--personal-main-account',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123@gmail.com',
            password='ilovemenotyou',
        )

        LoginCredential.objects.create(
            owner=user,
            service='steam--',
            name='Little Fries',
            slug='steam--little-fries',
            third_party_login=True,
            third_party_login_name='Personal Main Account',
            login='-----',
            password='-----',
        )

        SecurityNote.objects.create(
            owner=user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            content='Just draw an apple tree and erase the tree.',
        )

    def test_GET_anonymous_user(self) -> None:
        """GET / | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('home:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET / | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.client.login(username='user', password='passphrase')

        res: HttpResponse = self.client.get(reverse('home:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertIn('cards', res.context.keys())  # type: ignore
        self.assertIn('credentials', res.context.keys())  # type: ignore
        self.assertIn('notes', res.context.keys())  # type: ignore
        self.assertEqual(len(res.context['cards']), 1)
        self.assertEqual(len(res.context['credentials']), 2)
        self.assertEqual(len(res.context['notes']), 1)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
