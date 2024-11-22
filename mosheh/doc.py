from os import path

from constants import DEFAULT_MKDOCS_YML, FILE_MARKDOWN
from custom_types import CodebaseDict, Lang, NodeHandler, Statement


def generate_doc(
    codebase: CodebaseDict,
    exit: str,
    proj_name: str,
    lang: Lang,
    edit_uri: str = '',
    repo_name: str = 'GitHub',
    repo_url: str = '',
) -> None:
    # exit_path: str = path.abspath(exit)

    # try:
    #     result = subprocess.run(
    #         ['mkdocs', 'new', exit_path],
    #         check=True,
    #         capture_output=True,
    #         text=True,
    #     )
    #     print(result.stdout)
    # except subprocess.CalledProcessError as e:
    #     print('Error:', e.stderr)

    # with open(path.join(exit_path, 'mkdocs.yml'), 'w', encoding='utf-8') as f:
    #     f.write(
    #         default_doc_config(
    #             proj_name,
    #             edit_uri,
    #             lang.value,
    #             repo_name,
    #             repo_url,
    #         )
    #     )

    process_codebase(codebase)


def default_doc_config(
    proj_name: str,
    edit_uri: str,
    lang: str,
    repo_name: str = 'GitHub',
    repo_url: str = '',
) -> str:
    return DEFAULT_MKDOCS_YML.format(
        proj_name=proj_name,
        edit_uri=edit_uri,
        lang=lang,
        repo_name=repo_name,
        repo_url=repo_url,
    )


def codebase_file_to_markdown(filedata: list[NodeHandler], basedir: str) -> str:
    filename: str = basedir.split(path.sep)[-1]
    filepath: str = basedir.removesuffix(filename).replace(path.sep, '.')
    filedoc: str = ''
    imports: str = ''
    constants: str = ''
    classes: str = ''
    functions: str = ''
    assertions: str = ''

    for stmt in filedata:
        match stmt['statement']:
            case Statement.Import:
                mods = stmt['modules']

                for i in mods.keys():
                    imports += f'### `{i}`\n\nPath: `{mods[i]["path"]}`\n\nCategorie: {mods[i]["categorie"].value}\n\n'

            case Statement.ImportFrom:
                mods = stmt['modules']
                _path = stmt['path']
                categorie = stmt['categorie'].value

                for i in mods:
                    imports += (
                        f'### `{i}`\n\nPath: `{_path}`\n\nCategorie: {categorie}\n\n'
                    )

            case Statement.Assign:
                tokens: list[str] = stmt['tokens']
                for i in tokens:
                    constants += f'### `{i}`\n\nType: `Unknown`\n\nValue: `#!py {stmt["value"]}`\n\n'

            case Statement.AnnAssign:
                constants += f'### `{stmt["token"]}`\n\nType: `#!py {stmt["annot"]}`\n\nValue: `#!py {stmt["value"]}`\n\n'

            case Statement.ClassDef:
                parents: str = ', '.join(stmt['parents'])
                decorators: str = ', '.join(f'`#!py @{i}`' for i in stmt['decos'])
                if not decorators:
                    decorators = '`#!py None`'
                classes += f'### `{stmt["name"]}`\n\nParents: `{parents}`\n\nDecorators: {decorators}\n\nKwargs: {stmt["kwargs"]}\n\n'

            case Statement.FunctionDef:
                arg_lst_txt: str = ''
                decorators: str = ', '.join(f'`#!py @{i}`' for i in stmt['decos'])
                if not decorators:
                    decorators = '`#!py None`'
                if len(stmt['arg_lst']):
                    for i in stmt['arg_lst']:
                        name: str = i[0]
                        _type: str = i[1] if i[1] is not None else 'Unknown'
                        default: str = i[2]
                        if _type == 'str':
                            default = f"'{default}'"
                        arg_lst_txt += f'\n\n- `{name}`:\n\n\t- Type: `#!py {_type}`\n\n\t- Default: `#!py {default}`'
                else:
                    arg_lst_txt = 'No arguments at all.'
                functions += f'### `{stmt["name"]}`\n\nType: ...\n\nReturn Type: {stmt["rtype"]}\n\nDecorators: {decorators}\n\nArgs: {arg_lst_txt}\n\n'

            case Statement.Assert:
                assertion: str = ''
                msg: str = stmt['msg']
                if msg is not None:
                    msg = f"'{msg}'"
                if (
                    isinstance(stmt['test'], dict)
                    and stmt['test']['statement'] == Statement.Compare
                ):
                    asserts: list[tuple[str, int | str | NodeHandler]] = list(
                        zip(stmt['test']['ops'], stmt['test']['operators'])
                    )  # TODO confirm name -> stmt['operators'] after signal
                    _comps: list[str] = [f'{i[0]} {i[1]}' for i in asserts]
                    assertion = f'{stmt["test"]["left"]} ' + ' '.join(_comps)
                assertions += f'### `#!py assert {assertion}, {msg}`\n\n'

    return FILE_MARKDOWN.format(
        filename=filename,
        filepath=filepath,
        filedoc=filedoc,
        imports=imports,
        constants=constants,
        classes=classes,
        functions=functions,
        assertions=assertions,
    )


def process_codebase(
    codebase: dict[str, CodebaseDict] | dict[str, list[NodeHandler]],
    basedir: str = '',
):
    parents: list[str] = list(codebase.keys())

    for key in parents:
        value = codebase[key]
        new_path: str = path.join(basedir, key)

        if isinstance(value, list):
            if len(value):
                content: str = codebase_file_to_markdown(value, new_path)
                print(content)
            # Add to mkdos.yml > nav
            # Add to doc .md file
        else:
            process_codebase(value, new_path)
