from datetime import datetime
from warnings import filterwarnings

from django.core.exceptions import ValidationError
from django.db import DataError
from django.db.transaction import atomic
from django.test import TestCase

from account.models import ActivationAccountToken, User


class ActivationAccountTokenTestCase(TestCase):
    def setUp(self) -> None:
        filterwarnings('ignore', category=RuntimeWarning)

        self.user: User = User.objects.create_user(
            username='user',
            password='passphrase',
        )

        self.token1: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64, user=self.user, used=False
        )

        self.token2: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64, user=self.user, used=True
        )

        self.token3: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64, user=self.user, used=False, created=None
        )

        try:
            with atomic():
                self.token4: ActivationAccountToken = (
                    ActivationAccountToken.objects.create(
                        value='x' * 65, user=self.user, used=False
                    )
                )
        except DataError:
            self.token4: ActivationAccountToken = ActivationAccountToken.objects.create(
                value=int, user=self.user, used=False
            )

        self.token5: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 63, user=self.user, used=False
        )

    def test_token_instance_validity(self) -> None:
        """Tests token instance of correct class"""

        for token in ActivationAccountToken.objects.all():
            with self.subTest(token=token):
                self.assertIsInstance(token, ActivationAccountToken)

    def test_token_special_str_method_return(self) -> None:
        """Tests token return value of __str__ method"""

        token1: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token1.pk
        )

        self.assertEqual(token1.__str__(), 'x' * 64)

    def test_token_key_value_assertion(self) -> None:
        """Tests token correct attribuition of value"""

        token1: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token1.pk
        )

        self.assertEqual(token1.value, 'x' * 64)
        self.assertFalse(token1.used)
        self.assertIsInstance(token1.created, datetime)

    def test_token_create_validity(self) -> None:
        """Tests token creation integrity and validation"""

        token1: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token1.pk
        )
        token2: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token2.pk
        )
        token3: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token3.pk
        )
        token4: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token4.pk
        )
        token5: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token5.pk
        )

        self.assertEqual(ActivationAccountToken.objects.all().count(), 5)

        self.assertTrue(token1.is_valid())
        self.assertTrue(token2.is_valid())
        self.assertTrue(token3.is_valid())
        self.assertFalse(token4.is_valid())
        self.assertFalse(token5.is_valid())

    def test_token_update_validity(self) -> None:
        """Tests token update integrity and validation"""

        ActivationAccountToken.objects.filter(pk=self.token4.pk).update(
            value='x' * 64, created='2009-6-5'
        )

        ActivationAccountToken.objects.filter(pk=self.token5.pk).update(
            value='x' * 64, used=True
        )

        for token in ActivationAccountToken.objects.all():
            with self.subTest(token=token):
                self.assertTrue(token.is_valid())

    def test_token_delete_validity(self) -> None:
        """Tests token correct deletion"""

        for token in ActivationAccountToken.objects.all():
            if not token.is_valid():
                token.delete()

        self.assertEqual(ActivationAccountToken.objects.all().count(), 3)

    def test_token_db_exception_raises(self) -> None:
        """Tests token correct integrity and validation with raised exceptions"""

        # Expecting raises
        raise_kwargs: dict[str, dict[str, str | bool | int | None]] = {
            'token1': {'value': 'x' * 63},
            'token2': {'value': 'x' * 65},
            'token3': {'used': True},
            'token4': {'used': False},
            'token5': {'value': 'x' * 64, 'used': None},
            'token6': {'value': 'x' * 64, 'used': 'foo'},
            'token7': {'value': 'x' * 64, 'used': 2},
            'token8': {'value': 'x' * 64},
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance = ActivationAccountToken(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, str | User | bool | datetime]] = {
            'token1': {'value': 'x' * 64, 'user': self.user},
            'token2': {'value': 'x' * 64, 'user': self.user, 'used': False},
            'token3': {'value': 'x' * 64, 'user': self.user, 'used': True},
            'token4': {
                'value': 'x' * 64,
                'user': self.user,
                'created': datetime(2004, 5, 25),
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: ActivationAccountToken = ActivationAccountToken(
                    **no_raise_kwargs[scenario]
                )
                instance.full_clean()
