from argparse import ArgumentParser, Namespace
from os import path

from doc import Lang, generate_doc
from python import read_codebase


def main():
    parser: ArgumentParser = ArgumentParser(description='To be defined.')

    parser.add_argument('root', type=str, help='Root, base dir.')
    parser.add_argument('--lang', type=str, default='en', help='Path for doc output.')
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

    args: Namespace = parser.parse_args()

    ROOT: str = args.root
    PROJ_NAME: str = path.abspath(path.curdir).split(path.sep)[-1].upper()
    REPO_NAME: str = args.repo_name
    REPO_URL: str = args.repo_url
    EXIT: str = args.exit

    LANG: Lang = {'pt-BR': Lang.PT_BR, 'en': Lang.EN}.get(args.lang, Lang.EN)

    data: dict | None = read_codebase(ROOT)

    generate_doc(EXIT, PROJ_NAME, LANG, '', REPO_NAME, REPO_URL)


if __name__ == '__main__':
    main()
