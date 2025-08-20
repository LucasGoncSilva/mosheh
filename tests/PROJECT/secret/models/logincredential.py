from typing import Final
from uuid import uuid4

from account.models import User
from crypt import EncryptedCharField, EncryptedTextField
from django.core.validators import MaxLengthValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    UUIDField,
)
from django.template.defaultfilters import slugify
from django.urls import reverse

from secret.choices import credentials_services


class LoginCredential(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User, on_delete=CASCADE, related_name='credentials'
    )
    service: CharField = CharField(
        max_length=64,
        choices=credentials_services,
        validators=[MaxLengthValidator(64)],
    )
    name: CharField = CharField(
        max_length=40,
        validators=[MaxLengthValidator(40)],
    )
    third_party_login: BooleanField = BooleanField()
    third_party_login_name: EncryptedCharField = EncryptedCharField(
        validators=[MaxLengthValidator(40)],
    )
    login: EncryptedCharField = EncryptedCharField(
        validators=[MaxLengthValidator(200)],
    )
    password: EncryptedCharField = EncryptedCharField(
        validators=[MaxLengthValidator(200)]
    )
    note: EncryptedTextField = EncryptedTextField(
        max_length=128,
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
        return f'{str(self.owner.username)} | {self.service} | {self.name}'

    def get_absolute_url(self) -> str:
        return reverse('secret:credential_list_view')

    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {
            'service': 64,
            'name': 40,
            'slug': 128,
            'third_party_login_name': 40,
            'login': 200,
            'password': 200,
        }

        return max_length[var]

    def check_field_length(self, var: str) -> bool:
        value = self.__getattribute__(var)

        return len(value) <= self.expected_max_length(var)

    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = [
            'service',
            'name',
            'slug',
            'third_party_login_name',
            'login',
            'password',
        ]

        return all(map(self.check_field_length, vars))

    def all_fields_present(self) -> bool:
        if (
            self.owner
            and self.name
            and self.service in [slug for slug, _ in credentials_services]
            and self.slug == f'{self.service}{slugify(str(self.name))}'
            and self.third_party_login_name
            and self.login
            and self.password
        ):
            if (self.third_party_login and self.third_party_login_name != '-----') or (
                not self.third_party_login
                and self.login != '-----'
                and self.password != '-----'
            ):
                return True
        return False

    def all_fields_of_correct_types(self) -> bool:
        return [
            str(type(self.owner)),
            type(self.service),
            type(self.name),
            type(self.slug),
            type(self.third_party_login),
            type(self.third_party_login_name),
            type(self.login),
            type(self.password),
        ] == [
            "<class 'account.models.User'>",
            str,
            str,
            str,
            bool,
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
