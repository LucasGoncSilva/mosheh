from typing import Final
from uuid import uuid4

from account.models import User
from crypt import EncryptedCharField, EncryptedTextField
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    UUIDField,
)
from django.template.defaultfilters import slugify
from django.urls import reverse

from secret.choices import cards_banks, cards_brands, cards_types
from secret.month.models import MonthField


class PaymentCard(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE, related_name='cards')
    name: EncryptedCharField = EncryptedCharField(
        validators=[MaxLengthValidator(40)],
    )
    card_type: CharField = CharField(
        max_length=4,
        choices=cards_types,
        validators=[MaxLengthValidator(4)],
    )
    number: EncryptedCharField = EncryptedCharField(
        validators=[MinLengthValidator(12), MaxLengthValidator(19)],
    )
    expiration = MonthField()
    cvv: EncryptedCharField = EncryptedCharField(
        validators=[MinLengthValidator(3), MaxLengthValidator(4)],
    )
    bank: CharField = CharField(max_length=64, choices=cards_banks)
    brand: CharField = CharField(max_length=64, choices=cards_brands)
    owners_name: EncryptedCharField = EncryptedCharField(
        validators=[MaxLengthValidator(64)],
    )
    note: EncryptedTextField = EncryptedTextField(
        blank=True,
        null=True,
        validators=[MaxLengthValidator(128)],
    )
    slug: Final[SlugField] = SlugField(
        max_length=128, validators=[MaxLengthValidator(128)]
    )
    created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
    updated: Final[DateTimeField] = DateTimeField(auto_now=True)

    class Meta:
        ordering: Final[list[str]] = ['-created']

    def __str__(self) -> str:
        return f'{str(self.owner.username)} | {self.card_type} | {self.name}'

    def get_absolute_url(self) -> str:
        return reverse('secret:card_list_view')

    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {
            'name': 40,
            'card_type': 16,
            'number': 19,
            'cvv': 4,
            'bank': 64,
            'brand': 64,
            'slug': 128,
            'owners_name': 64,
            'note': 128,
        }

        return max_length[var]

    def expected_min_length(self, var: str) -> int:
        min_length: Final[dict[str, int]] = {
            'number': 12,
            'cvv': 3,
        }

        return min_length[var]

    def check_field_length(self, var: str) -> bool:
        if var == 'expiration':
            return True

        value = self.__getattribute__(var)

        if var in ['number', 'cvv']:
            return (
                self.expected_min_length(var)
                <= len(value)
                <= self.expected_max_length(var)
            )

        return len(value) <= self.expected_max_length(var)

    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = [
            'name',
            'card_type',
            'number',
            'expiration',
            'cvv',
            'bank',
            'brand',
            'slug',
            'owners_name',
        ]

        return all(map(self.check_field_length, vars))

    def all_fields_present(self) -> bool:
        return bool(
            self.owner
            and self.name
            and self.card_type in [slug for slug, _ in cards_types]
            and self.number
            and self.expiration
            and self.cvv
            and self.bank in [slug for slug, _ in cards_banks]
            and self.brand in [slug for slug, _ in cards_brands]
            and self.owners_name
            and self.slug == f'{self.bank}{slugify(str(self.name))}'
        )

    def all_fields_of_correct_types(self) -> bool:
        return [
            str(type(self.owner)),
            type(self.name),
            type(self.card_type),
            type(self.number),
            str(type(self.expiration)),
            type(self.cvv),
            type(self.bank),
            type(self.brand),
            type(self.slug),
            type(self.owners_name),
        ] == [
            "<class 'account.models.User'>",
            str,
            str,
            str,
            "<class 'secret.month.Month'>",
            str,
            str,
            str,
            str,
            str,
        ]

    def is_valid(self) -> bool:
        if (
            self.all_fields_present()
            and self.all_fields_of_correct_types()
            and self.all_fields_of_right_length()
        ):
            return True
        return False
