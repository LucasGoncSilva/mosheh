from argparse import ArgumentParser
from ast import Call, Name, parse
from ast import walk as astwalk
from os import path, walk
from types import ModuleType, SimpleNamespace


def main():
    parser: ArgumentParser = ArgumentParser(description='To be defined.')

    parser.add_argument('root', type=str, help='Root, base dir.')

    args: SimpleNamespace = parser.parse_args()

    call_name: str = 'ExampleTest'

    total: int = count_calls(args.root, call_name)
    print(f"'{call_name}' was called {total}x")


def count_calls(dir_name: str, callable: str) -> int:
    count: int = 0

    for dirpath, _, files in walk(dir_name):
        for file in files:
            if file.endswith('.py'):
                f_path: str = path.join(dirpath, file)

                with open(f_path, encoding='utf-8') as f:
                    codigo: str = f.read()

                arvore: ModuleType = parse(codigo, filename=f_path)

                for node in astwalk(arvore):
                    if isinstance(node, Call):
                        if isinstance(node.func, Name) and node.func.id == callable:
                            count += 1

    return count


if __name__ == '__main__':
    main()
