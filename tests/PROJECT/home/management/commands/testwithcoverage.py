from os import system
from typing import Any, Literal

from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='App to be covered - "." if nothing is defined.',
            default='.',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        omit_list: list[str] = [
            '*/month/*,',
            '*/migrations/*,',
            '*/admin.py,',
            'manage.py,',
            '*/CORE/*,',
        ]

        app: Literal['.'] | str = options['app']
        source: str = f"--source='{app}'"
        omit: str = f"--omit='{','.join(omit_list)}'"
        cmd: str = f'coverage run {source} {omit} manage.py test {app}'

        system(cmd)
        system('coverage html')

        self.stdout.write(self.style.SUCCESS('Coverage done + HTML file generated.'))
