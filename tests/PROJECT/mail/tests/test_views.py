from account.models import User
from django.contrib.auth import get_user
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class WakeDatabaseViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='passphrase',
            is_active=True,
        )

        self.ENDPOINT: str = reverse('mail:wake')

    def test_GET_anonymous_user(self) -> None:
        """GET /enviar-email/wake | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.ENDPOINT)

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /enviar-email/wake | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='passphrase'))

        res: HttpResponse = self.client.get(self.ENDPOINT)

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user(self) -> None:
        """POST /enviar-email/wake | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            self.ENDPOINT, {'DATA': 'HERE'}, follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Logged user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user(self) -> None:
        """POST /enviar-email/wake | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='passphrase'))

        res: HttpResponse = self.client.post(
            self.ENDPOINT, {'DATA': 'HERE'}, follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_return_values(self) -> None:
        """POST /enviar-email/wake | return values based on num of reqs"""

        for i in range(1, 17):
            with self.subTest(i=i):
                res: HttpResponse = self.client.get(self.ENDPOINT)
                self.assertEqual(int(res.content), i % 4)
