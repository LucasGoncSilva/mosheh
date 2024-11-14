from argparse import ArgumentParser
from os import path
from types import SimpleNamespace

from doc import Lang, generate_doc
from python import count_calls


def main():
    parser: ArgumentParser = ArgumentParser(description='To be defined.')

    parser.add_argument('root', type=str, help='Root, base dir.')
    parser.add_argument(
        '--lang', type=str, default=Lang.EN, help='Path for doc output.'
    )
    parser.add_argument(
        '--repo-name',
        type=str,
        default='GitHub',
        help='Repo name.',
    )
    parser.add_argument(
        '--repo-url',
        type=str,
        default='https://github.com/',
        help='Repo URL.',
    )
    parser.add_argument('--exit', type=str, default='.', help='Path for doc output')

    args: SimpleNamespace = parser.parse_args()

    ROOT: str = args.root
    PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
    LANG: str = args.lang
    REPO_NAME: str = args.repo_name
    REPO_URL: str = args.repo_url
    EXIT: str = args.exit

    call_name: str = 'ExampleTest'

    total: int = count_calls(ROOT, call_name)
    print(f"'{call_name}' was called {total}x")

    generate_doc(EXIT, PROJ_NAME, '', LANG, REPO_NAME, REPO_URL)


if __name__ == '__main__':
    main()
