from account.models import User
from django.core.exceptions import ValidationError
from django.db import DataError
from django.db.transaction import atomic
from django.test import TestCase
from django.urls import reverse
from utils import create_scenarios, xor

from secret.models import LoginCredential, PaymentCard, SecurityNote
from secret.month.models import Month


class CredentialTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='passphrase',
        )

        # Object 1
        self.login_credential_1: LoginCredential = LoginCredential.objects.create(
            owner=self.user,
            service='google--',
            name='Personal Main Account',
            slug='google--personal-main-account',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123@gmail.com',
            password='ilovemenotyou',
        )  # Correct object

        # Object 2
        self.login_credential_2: LoginCredential = LoginCredential.objects.create(
            owner=self.user,
            service='steam--',
            name='Little Fries',
            slug='steam--little-fries',
            third_party_login=True,
            third_party_login_name='Personal Main Account',
            login='-----',
            password='-----',
        )  # Correct object

        # Object 3
        self.login_credential_3: LoginCredential = LoginCredential.objects.create(
            owner=self.user,
            service='steam--',
            name='Little Fries',
            slug='steam--little-fries',
            third_party_login=True,  # False or...
            third_party_login_name='-----',  # something different to '-----'
            login='night_monkey123',  # '-----'
            password='ilovemenotyou',  # '-----'
        )

        # Object 4
        self.login_credential_4: LoginCredential = LoginCredential.objects.create(
            owner=self.user,
            service='steam--',
            name='Little Fries',
            slug='steam--potato',  # 'steam--little-fries'
            third_party_login=False,
            third_party_login_name='-----',
            login='',  # Empty login
            password='night_monkey123',
        )

        # Object 5
        self.login_credential_5: LoginCredential = LoginCredential.objects.create(
            owner=self.user,
            service='steam--',
            name='Little Fries',
            slug='steam--little-fries',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123',
            # Missing/empty password field
        )

        # Object 6
        try:
            with atomic():
                self.login_credential_6: LoginCredential = (
                    LoginCredential.objects.create(
                        owner=self.user,
                        service='google--',
                        name='Salve' * 9,  # More chars than the limit
                        slug='google--personal-main-account',
                        third_party_login=False,
                        third_party_login_name='-----',
                        login='x' * 201,  # More chars than the limit
                        password='ilovemenotyou',
                    )
                )
        except DataError:
            self.login_credential_6: LoginCredential = LoginCredential.objects.create(
                owner=self.user,
                service='steam--',
                name='Little Fries',
                slug='steam--little-fries',
                third_party_login=False,
                third_party_login_name='-----',
                login='night_monkey123',
                # Missing/empty password field
            )

        # Object 7
        self.login_credential_7: LoginCredential = LoginCredential.objects.create(
            owner=self.user,
            service='pampas-gonden-radio--',  # Inexistent service
            name='Little Fries',
            slug='pampas-gonden-radio--little-fries',
            third_party_login=True,
            third_party_login_name='Personal Main Account',
            login='-----',
            password='-----',
        )

    def test_credential_instance_validity(self) -> None:
        """Tests credential instance of correct class"""

        for cred in LoginCredential.objects.all():
            with self.subTest(cred=cred):
                self.assertIsInstance(cred, LoginCredential)

    def test_credential_key_value_assertion(self) -> None:
        """Tests credential correct attribuition of value"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1.pk
        )

        self.assertEqual(cred1.service, 'google--')
        self.assertEqual(cred1.name, 'Personal Main Account')
        self.assertEqual(cred1.slug, 'google--personal-main-account')
        self.assertFalse(cred1.third_party_login)
        self.assertEqual(cred1.third_party_login_name, '-----')
        self.assertEqual(cred1.login, 'night_monkey123@gmail.com')
        self.assertEqual(cred1.password, 'ilovemenotyou')

    def test_credential_special_str_method_return(self) -> None:
        """Tests credential return value of __str__ method"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1.pk
        )

        self.assertEqual(
            cred1.__str__(),
            f'{str(cred1.owner.username)} | {cred1.service} | {cred1.name}',
        )

    def test_credential_absolute_url_method_return(self) -> None:
        """Tests credential return value of get_absolute_url method"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1.pk
        )

        self.assertEqual(
            cred1.get_absolute_url(), reverse('secret:credential_list_view')
        )

    def test_credential_user_foreign_key_validity(self) -> None:
        """Tests credential foreign key validation"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1.pk
        )
        cred2: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_2.pk
        )

        cred1_owner: User = cred1.owner
        cred2_owner: User = cred2.owner

        self.assertEqual(cred1_owner, cred2_owner)
        self.assertEqual(cred1_owner, self.user)

    def test_credential_create_validity(self) -> None:
        """Tests credential creation integrity and validation"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1.pk
        )
        cred2: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_2.pk
        )
        cred3: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_3.pk
        )
        cred4: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_4.pk
        )
        cred5: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_5.pk
        )
        cred6: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_6.pk
        )
        cred7: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_7.pk
        )

        self.assertEqual(LoginCredential.objects.all().count(), 7)

        self.assertTrue(cred1.is_valid())
        self.assertTrue(cred2.is_valid())
        self.assertFalse(cred3.is_valid())
        self.assertFalse(cred4.is_valid())
        self.assertFalse(cred5.is_valid())
        self.assertFalse(cred6.is_valid())
        self.assertFalse(cred7.is_valid())

    def test_credential_update_validity(self) -> None:
        """Tests credential update integrity and validation"""

        LoginCredential.objects.filter(pk=self.login_credential_3.pk).update(
            third_party_login=False
        )
        LoginCredential.objects.filter(pk=self.login_credential_4.pk).update(
            slug='steam--little-fries',
            login='some_login_text_or_email_or_some_other_stuff_like_this',
        )
        LoginCredential.objects.filter(pk=self.login_credential_5.pk).update(
            password='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        LoginCredential.objects.filter(pk=self.login_credential_6.pk).update(
            password='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        LoginCredential.objects.filter(pk=self.login_credential_7.pk).update(
            service='visa--', slug='visa--little-fries'
        )

        for cred in LoginCredential.objects.all():
            with self.subTest(cred=cred):
                self.assertTrue(cred.is_valid())

    def test_credential_delete_validity(self) -> None:
        """Tests credential correct deletion"""

        for cred in LoginCredential.objects.all():
            if not cred.is_valid():
                cred.delete()

        self.assertEqual(LoginCredential.objects.all().count(), 2)

    def test_credential_db_exception_raises(self) -> None:
        """Tests credential correct integrity and validation with raised exceptions"""

        # Expecting raises
        params: list[dict[str, User | str | bool]] = [
            {'owner': self.user},
            {'service': 'aws--'},
            {'name': 'Name'},
            {'third_party_login': False},
            {'third_party_login_name': '-----'},
            {'login': 'LoginName'},
            {'password': 'PasswordName'},
            {'slug': 'aws--name'},
        ]

        for case, scenario in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: LoginCredential = LoginCredential(**scenario)
                        instance.full_clean()

        raise_kwargs: dict[str, dict[str, User | str | bool]] = {
            'cred1': {
                'owner': self.user,
                'service': 'aws--',
                'name': 'x' * 41,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred2': {
                'owner': self.user,
                'service': 'aws--',
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 41,
                'login': 'x' * 201,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred3': {
                'owner': self.user,
                'service': 'aws--',
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 201,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred4': {
                'owner': self.user,
                'service': 'aws--',
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 129,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred5': {
                'owner': self.user,
                'service': 'aws--',
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 124,
            },
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: LoginCredential = LoginCredential(
                            **raise_kwargs[scenario]
                        )
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, User | str | bool]] = {
            'cred1': {
                'owner': self.user,
                'service': 'aws--',
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 123,
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: LoginCredential = LoginCredential(**no_raise_kwargs[scenario])
                instance.full_clean()


class CardTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='passphrase',
        )

        # Object 1
        self.card_1: PaymentCard = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card One',
            card_type='deb',
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank='nubank--',
            brand='mastercard--',
            slug='nubank--personal-main-card-one',
            owners_name='TEST USER',
        )  # Correct object

        # Object 2
        try:
            with atomic():
                self.card_2: PaymentCard = PaymentCard.objects.create(
                    owner=self.user,
                    name='Personal Main Card',
                    card_type='creda',  # Inexintent type and more chars than the limit
                    number='4002892240028922',
                    expiration=Month(2028, 11),
                    cvv=113,
                    bank='nubank--',
                    brand='mastercard--',
                    slug='nubank--personal-main-card',
                    owners_name='TEST USER',
                )
        except DataError:
            self.card_2: PaymentCard = PaymentCard.objects.create(
                owner=self.user,
                name='Personal Main Card Two',
                card_type='baka',  # Inexintent type
                number='4002892240028922',
                expiration=Month(2028, 11),
                cvv=113,
                bank='nubank--',
                brand='mastercard--',
                slug='nubank--personal-main-card-two',
                owners_name='TEST USER',
            )

        # Object 3
        self.card_3: PaymentCard = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card Three',
            card_type='deb',
            number='123456789',  # Length out of range
            expiration=Month(2028, 11),
            cvv=12,  # Length out of range
            bank='nubank--',
            brand='mastercard--',
            slug='nubank--personal-main-card-three',
            owners_name='TEST USER',
        )

        # Object 4
        self.card_4: PaymentCard = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card Four',
            card_type='deb',
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv=113,
            bank='mingau--',  # Inexistent bank
            brand='mastercard--',
            slug='mingau--personal-main-card-four',
            owners_name='TEST USER',
        )

        # Object 5
        self.card_5: PaymentCard = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card Five',
            card_type='deb',
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank='nubank--',
            brand='mastercard--',
            slug='nubank--personal-not-main-card',  # 'nubank--personal-main-card-five'
            owners_name='TEST USER',
        )

        # Object 6
        self.card_6: PaymentCard = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card Six',
            card_type='deb',
            number='4002892240028922',
            expiration='2023/4',
            cvv=113,
            bank='nubank--',
            brand='vina--',  # Inexistent brand
            slug='nubank--personal-main-card-six',
            owners_name='TEST USER',
        )

    def test_card_instance_validity(self) -> None:
        """Tests card instance of correct class"""

        for card in PaymentCard.objects.all():
            with self.subTest(card=card):
                self.assertIsInstance(card, PaymentCard)

    def test_card_special_str_method_return(self) -> None:
        """Tests card return value of __str__ method"""

        card1: PaymentCard = PaymentCard.objects.get(pk=self.card_1.pk)

        self.assertEqual(
            card1.__str__(),
            f'{str(card1.owner.username)} | {card1.card_type} | {card1.name}',
        )

    def test_card_absolute_url_method_return(self) -> None:
        """Tests card return value of get_absolute_url method"""

        cred1: PaymentCard = PaymentCard.objects.get(pk=self.card_1.pk)

        self.assertEqual(cred1.get_absolute_url(), reverse('secret:card_list_view'))

    def test_card_key_value_assertion(self) -> None:
        """Tests card correct attribuition of value"""

        card1: PaymentCard = PaymentCard.objects.get(pk=self.card_1.pk)

        self.assertEqual(card1.name, 'Personal Main Card One')
        self.assertEqual(card1.card_type, 'deb')
        self.assertEqual(card1.number, '4002892240028922')
        self.assertEqual(card1.expiration, Month(2028, 11))
        self.assertEqual(card1.cvv, '113')
        self.assertEqual(card1.bank, 'nubank--')
        self.assertEqual(card1.brand, 'mastercard--')
        self.assertEqual(card1.slug, 'nubank--personal-main-card-one')
        self.assertEqual(card1.owners_name, 'TEST USER')

    def test_card_user_foreign_key_validity(self) -> None:
        """Tests card foreign key validation"""

        card1_owner: User = PaymentCard.objects.get(pk=self.card_1.pk).owner

        self.assertEqual(card1_owner, self.user)

    def test_card_create_validity(self) -> None:
        """Tests card creation integrity and validation"""

        card1: PaymentCard = PaymentCard.objects.get(pk=self.card_1.pk)
        card2: PaymentCard = PaymentCard.objects.get(pk=self.card_2.pk)
        card3: PaymentCard = PaymentCard.objects.get(pk=self.card_3.pk)
        card4: PaymentCard = PaymentCard.objects.get(pk=self.card_4.pk)
        card5: PaymentCard = PaymentCard.objects.get(pk=self.card_5.pk)
        card6: PaymentCard = PaymentCard.objects.get(pk=self.card_6.pk)

        self.assertEqual(PaymentCard.objects.all().count(), 6)

        self.assertTrue(card1.is_valid())
        self.assertFalse(card2.is_valid())
        self.assertFalse(card3.is_valid())
        self.assertFalse(card4.is_valid())
        self.assertFalse(card5.is_valid())
        self.assertFalse(card6.is_valid())

    def test_card_update_validity(self) -> None:
        """Tests card update integrity and validation"""

        PaymentCard.objects.filter(pk=self.card_2.pk).update(card_type='cred')
        PaymentCard.objects.filter(pk=self.card_3.pk).update(
            number=xor('1122334455667788', self.user.password[21:]),
            cvv=xor('1986', self.user.password[21:]),
        )
        PaymentCard.objects.filter(pk=self.card_4.pk).update(
            bank='pagseguro--',
            slug='pagseguro--personal-main-card-four',
        )
        PaymentCard.objects.filter(pk=self.card_5.pk).update(
            slug='nubank--personal-main-card-five'
        )
        PaymentCard.objects.filter(pk=self.card_6.pk).update(brand='mastercard--')

        for i, card in enumerate(PaymentCard.objects.all(), start=1):
            with self.subTest(card=i):
                self.assertTrue(card.is_valid())

    def test_card_delete_validity(self) -> None:
        """Tests card correct deletion"""

        for card in PaymentCard.objects.all():
            if not card.is_valid():
                card.delete()

        self.assertEqual(PaymentCard.objects.all().count(), 1)

    def test_card_db_exception_raises(self) -> None:
        """Tests card correct integrity and validation with raised exceptions"""

        # Expecting raises
        params: list[dict[str, User | str]] = [
            {'owner': self.user},
            {'name': 'Name'},
            {'card_type': 'deb'},
            {'number': '1111222233334444'},
            {'cvv': '044'},
            {'bank': 'nubank--'},
            {'brand': 'visa--'},
            {'owners_name': "Owner's Name"},
            {'slug': 'name'},
        ]

        for case, scenario in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: PaymentCard = PaymentCard(**scenario)
                        instance.full_clean()

        raise_kwargs: dict[str, dict[str, str | Month | User]] = {
            'card1': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 4,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 41,
            },
            'card2': {
                'owner': self.user,
                'name': 'x' * 41,
                'card_type': 'x' * 4,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
            'card3': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 5,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
            'card4': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 4,
                'number': 'x' * 11,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
            'card5': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 4,
                'number': 'x' * 20,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
            'card6': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 4,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 2,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
            'card7': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 4,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 5,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
            'card8': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 4,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 65,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
            'card9': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'x' * 4,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 129,
                'slug': 'x' * 40,
            },
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: PaymentCard = PaymentCard(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, str | Month | User]] = {
            'card1': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': 'cred',
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': 'nubank--',
                'brand': 'visa--',
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': 'x' * 40,
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: PaymentCard = PaymentCard(**no_raise_kwargs[scenario])
                instance.full_clean()


class SecurityNoteTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='passphrase',
        )

        # Object 1
        self.security_note_1: SecurityNote = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            note_type='hlt',
            content='Just draw an apple tree and erase the tree.',
        )  # Correct object

        # Object 2
        self.security_note_2: SecurityNote = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw a tree',
            slug='howtodrawatree',  # 'how-to-draw-a-tree'
            note_type='hlt',
            content='Just draw an apple tree and erase the apples.',
        )

        # Object 3
        self.security_note_3: SecurityNote = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple tree',
            slug='how-to-draw-an-apple-tree',
            note_type='hlt',
            content='x' * 1001,  # Length out of range
        )

        # Object 4
        self.security_note_4: SecurityNote = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple tree leaf',
            slug='how-to-draw-an-apple-tree-leaf',
            note_type='hlt',
        )  # Missing/empty content field

        # Object 5
        self.security_note_5: SecurityNote = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            note_type='outro',  # Length out of range
            content='Just draw an apple tree and erase the tree.',
        )

    def test_note_instance_validity(self) -> None:
        """Tests note instance of correct class"""

        for note in SecurityNote.objects.all():
            with self.subTest(note=note):
                self.assertIsInstance(note, SecurityNote)

    def test_note_special_str_method_return(self) -> None:
        """Tests note return value of __str__ method"""

        note1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1.pk)

        self.assertEqual(
            note1.__str__(), f'{str(note1.owner.username)} | {note1.title}'
        )

    def test_note_absolute_url_method_return(self) -> None:
        """Tests note return value of get_absolute_url method"""

        cred1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1.pk)

        self.assertEqual(cred1.get_absolute_url(), reverse('secret:note_list_view'))

    def test_note_key_value_assertion(self) -> None:
        """Tests note correct attribuition of value"""

        note1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1.pk)

        self.assertEqual(note1.title, 'How to draw an apple')
        self.assertEqual(note1.slug, 'how-to-draw-an-apple')
        self.assertEqual(note1.note_type, 'hlt')
        self.assertEqual(note1.content, 'Just draw an apple tree and erase the tree.')

    def test_note_user_foreign_key_validity(self) -> None:
        """Tests note foreign key validation"""

        note1_owner: User = SecurityNote.objects.get(pk=self.security_note_1.pk).owner

        self.assertEqual(note1_owner, self.user)

    def test_note_create_validity(self) -> None:
        """Tests note creation integrity and validation"""

        note1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1.pk)
        note2: SecurityNote = SecurityNote.objects.get(pk=self.security_note_2.pk)
        note3: SecurityNote = SecurityNote.objects.get(pk=self.security_note_3.pk)
        note4: SecurityNote = SecurityNote.objects.get(pk=self.security_note_4.pk)
        note5: SecurityNote = SecurityNote.objects.get(pk=self.security_note_5.pk)

        self.assertEqual(SecurityNote.objects.all().count(), 5)

        self.assertTrue(note1.is_valid())
        self.assertFalse(note2.is_valid())
        self.assertFalse(note3.is_valid())
        self.assertFalse(note4.is_valid())
        self.assertFalse(note5.is_valid())

    def test_note_update_validity(self) -> None:
        """Tests note update integrity and validation"""

        SecurityNote.objects.filter(pk=self.security_note_2.pk).update(
            slug='how-to-draw-a-tree'
        )
        SecurityNote.objects.filter(pk=self.security_note_3.pk).update(
            content='Draw a tree and then the apples.'
        )
        SecurityNote.objects.filter(pk=self.security_note_4.pk).update(
            content='Draw an apple tree and then erase the apples and the tree.'
        )
        SecurityNote.objects.filter(pk=self.security_note_5.pk).update(note_type='oth')

        for note in SecurityNote.objects.all():
            with self.subTest(note=note):
                self.assertTrue(note.is_valid())

    def test_note_delete_validity(self) -> None:
        """Tests note correct deletion"""

        for note in SecurityNote.objects.all():
            if not note.is_valid():
                note.delete()

        self.assertEqual(SecurityNote.objects.all().count(), 1)

    def test_note_db_exception_raises(self) -> None:
        """Tests note correct integrity and validation with raised exceptions"""

        # Expecting raises
        raise_kwargs: dict[str, dict[str, User | str]] = {
            'note1': {'owner': self.user},
            'note2': {'title': 'A Title'},
            'note3': {'slug': 'a-title'},
            'note4': {'note_type': 'std'},
            'note5': {'content': 'A regular content'},
            'note6': {'owner': self.user, 'title': 'A Title'},
            'note7': {'owner': self.user, 'slug': 'a-title'},
            'note8': {'owner': self.user, 'content': 'A regular content'},
            'note9': {'owner': self.user, 'note_type': 'std'},
            'note10': {'owner': self.user, 'title': 'A Title', 'slug': 'a-title'},
            'note11': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
            },
            'note12': {
                'owner': self.user,
                'title': 'A Title',
                'note_type': 'std',
            },
            'note13': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
                'slug': 'a-title',
            },
            'note14': {
                'owner': self.user,
                'title': 'x' * 41,
                'content': 'A regular content',
                'slug': 'a-title',
                'note_type': 'std',
            },
            'note15': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'x' * 1001,
                'slug': 'a-title',
                'note_type': 'std',
            },
            'note16': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
                'slug': 'x' * 51,
                'note_type': 'std',
            },
            'note17': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
                'slug': 'a-title',
                'note_type': 'none',
            },
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: SecurityNote = SecurityNote(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, str | User]] = {
            'note1': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
                'note_type': 'std',
                'slug': 'a-title',
            },
            'note2': {
                'owner': self.user,
                'title': 'x ' * 20,
                'content': 'x' * 300,
                'note_type': 'wrk',
                'slug': 'x-' * 20,
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: SecurityNote = SecurityNote(**no_raise_kwargs[scenario])
                instance.full_clean()
