from random import choices
from typing import Any, Self

from account.models import User
from django.core.management import BaseCommand
from django.utils.text import slugify
from secret.models import LoginCredential, PaymentCard, SecurityNote
from secret.month.models import Month
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self: Self, *args: Any, **options: Any) -> None:
        self.populate_cards()
        self.populate_notes()
        self.populate_credentials()

    def populate_cards(self: Self) -> None:
        if PaymentCard.objects.filter(slug='other--rdias').exists():
            self.stdout.write('secret.PaymentCard is already populated')
            return

        self.stdout.write('\nPopulating secret.PaymentCard')

        with open('./secret/management/commands/populatecard.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))

        for i, data in tqdm(
            enumerate(f),
            desc='Payment Cards',
            bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}',
            total=500,
        ):
            (
                name,
                card_type,
                number,
                expiration,
                cvv,
                bank,
                brand,
                owners_name,
                note,
            ) = data

            owner: User = User.objects.get(pk=owners_ids[i])

            y, m = expiration.split('-')
            expiration: Month = Month(int(y), int(m))

            PaymentCard.objects.create(
                owner=owner,
                name=name,
                card_type=card_type,
                number=number,
                expiration=expiration,
                cvv=cvv,
                bank=bank,
                brand=brand,
                owners_name=owners_name,
                note=note,
                slug=f'{bank}{slugify(name)}',
            )

    def populate_notes(self: Self) -> None:
        if SecurityNote.objects.filter(slug='dolorem-mo').exists():
            self.stdout.write('secret.SecurityNote is already populated')
            return

        self.stdout.write('\nPopulating secret.SecurityNote')

        with open('./secret/management/commands/populatenote.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))

        for i, data in tqdm(
            enumerate(f),
            desc='Security Notes',
            bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}',
            total=500,
        ):
            title, note_type, content = data

            owner = User.objects.get(pk=owners_ids[i])

            SecurityNote.objects.create(
                owner=owner,
                title=title,
                note_type=note_type,
                content=content,
                slug=slugify(title),
            )

    def populate_credentials(self: Self) -> None:
        if LoginCredential.objects.filter(slug='discord--giovanna-cardoso').exists():
            self.stdout.write('secret.LoginCredential is already populated')
            return

        self.stdout.write('\nPopulating secret.LoginCredential')

        with open('./secret/management/commands/populatecredential.txt') as sample:
            f: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        owners_ids: list[User] = choices([i.id for i in User.objects.all()], k=len(f))

        for i, data in tqdm(
            enumerate(f),
            desc='Login Credentials',
            bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}',
            total=500,
        ):
            (
                service,
                name,
                third_party_login,
                third_party_login_name,
                login,
                password,
                note,
            ) = data

            owner = User.objects.get(pk=owners_ids[i])

            LoginCredential.objects.create(
                owner=owner,
                service=service,
                name=name,
                third_party_login=third_party_login,
                third_party_login_name=third_party_login_name,
                login=login,
                password=password,
                note=note,
                slug=f'{service}{slugify(name)}',
            )
