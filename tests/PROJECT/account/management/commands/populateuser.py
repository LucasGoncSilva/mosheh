from typing import Any

from account.models import User
from django.core.management import BaseCommand
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        if User.objects.filter(username='ernestodruso').exists():
            self.stdout.write('\naccount.User is already populated')
            return

        self.stdout.write('\nPopulating account.User')

        with open('./account/management/commands/populateuser.txt') as sample:
            lines: list[list[str]] = [i.strip().split('::') for i in sample.readlines()]

        for i in tqdm(
            lines, desc='Users', bar_format='{l_bar}{bar:100}{r_bar}{bar:-10b}'
        ):
            username, passphrase = i
            user: User = User.objects.create_user(  # type: ignore
                username=username, password=passphrase
            )

            user.is_active = True

            user.save()
