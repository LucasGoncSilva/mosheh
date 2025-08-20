from typing import Final
from uuid import uuid4

from account.models import User
from crypt import EncryptedTextField
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    SlugField,
    TextField,
    UUIDField,
)
from django.template.defaultfilters import slugify
from django.urls import reverse

from secret.choices import notes_types


class SecurityNote(Model):
    id: Final[UUIDField] = UUIDField(
        default=uuid4, unique=True, primary_key=True, editable=False
    )
    owner: Final[ForeignKey] = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='notes',
    )
    title: Final[CharField] = CharField(
        max_length=40, validators=[MaxLengthValidator(40)]
    )
    content: EncryptedTextField = EncryptedTextField(
        validators=[MaxLengthValidator(1000)]
    )
    note_type: Final[TextField] = TextField(
        max_length=3,
        choices=notes_types,
        validators=[MaxLengthValidator(3), MinLengthValidator(3)],
    )
    slug: Final[SlugField] = SlugField(
        max_length=50, validators=[MaxLengthValidator(50)]
    )
    created: Final[DateTimeField] = DateTimeField(
        auto_now_add=True,
    )
    updated: Final[DateTimeField] = DateTimeField(
        auto_now=True,
    )

    def __str__(self) -> str:
        return f'{str(self.owner.username)} | {self.title}'

    def get_absolute_url(self) -> str:
        return reverse('secret:note_list_view')

    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {
            'title': 40,
            'content': 1000,
            'note_type': 3,
            'slug': 50,
        }

        return max_length[var]

    def check_field_length(self, var: str) -> bool:
        value = self.__getattribute__(var)

        return len(value) <= self.expected_max_length(var)

    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = [
            'title',
            'content',
            'note_type',
            'slug',
        ]

        return all(map(self.check_field_length, vars))

    def all_fields_present(self) -> bool:
        return bool(
            self.owner
            and self.title
            and self.content
            and self.note_type
            and self.slug == slugify(str(self.title))
        )

    def all_fields_of_correct_types(self) -> bool:
        return [
            str(type(self.owner)),
            type(self.title),
            type(self.content),
            type(self.note_type),
            type(self.slug),
        ] == [
            "<class 'account.models.User'>",
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

    class Meta:
        ordering: Final[list[str]] = ['-created']
