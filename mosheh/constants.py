from typing import Final


BUILTIN_MODULES: Final[list[str]] = [
    '__future__',
    '_abc',
    '_aix_support',
    '_ast',
    '_asyncio',
    '_bisect',
    '_blake2',
    '_bootsubprocess',
    '_bz2',
    '_codecs',
    '_codecs_cn',
    '_codecs_hk',
    '_codecs_iso2022',
    '_codecs_jp',
    '_codecs_kr',
    '_codecs_tw',
    '_collections',
    '_collections_abc',
    '_compat_pickle',
    '_compression',
    '_contextvars',
    '_crypt',
    '_csv',
    '_ctypes',
    '_ctypes_test',
    '_curses',
    '_curses_panel',
    '_datetime',
    '_dbm',
    '_decimal',
    '_distutils_hack',
    '_distutils_system_mod',
    '_elementtree',
    '_functools',
    '_gdbm',
    '_hashlib',
    '_heapq',
    '_imp',
    '_io',
    '_json',
    '_locale',
    '_lsprof',
    '_lzma',
    '_markupbase',
    '_md5',
    '_multibytecodec',
    '_multiprocessing',
    '_opcode',
    '_operator',
    '_osx_support',
    '_pickle',
    '_posixshmem',
    '_posixsubprocess',
    '_py_abc',
    '_pydecimal',
    '_pyio',
    '_queue',
    '_random',
    '_sha1',
    '_sha256',
    '_sha3',
    '_sha512',
    '_signal',
    '_sitebuiltins',
    '_socket',
    '_sqlite3',
    '_sre',
    '_ssl',
    '_stat',
    '_statistics',
    '_string',
    '_strptime',
    '_struct',
    '_symtable',
    '_sysconfigdata__linux_x86_64-linux-gnu',
    '_sysconfigdata__x86_64-linux-gnu',
    '_testbuffer',
    '_testcapi',
    '_testclinic',
    '_testimportmultiple',
    '_testinternalcapi',
    '_testmultiphase',
    '_thread',
    '_threading_local',
    '_tracemalloc',
    '_uuid',
    '_warnings',
    '_weakref',
    '_weakrefset',
    '_xxsubinterpreters',
    '_xxtestfuzz',
    '_zoneinfo',
    'abc',
    'aifc',
    'antigravity',
    'argparse',
    'array',
    'ast',
    'asynchat',
    'asyncio',
    'asyncore',
    'atexit',
    'audioop',
    'base64',
    'bdb',
    'binascii',
    'binhex',
    'bisect',
    'builtins',
    'bz2',
    'cProfile',
    'calendar',
    'cgi',
    'cgitb',
    'chunk',
    'cmath',
    'cmd',
    'code',
    'codecs',
    'codeop',
    'collections',
    'colorsys',
    'compileall',
    'concurrent',
    'configparser',
    'contextlib',
    'contextvars',
    'copy',
    'copyreg',
    'crypt',
    'csv',
    'ctypes',
    'curses',
    'dataclasses',
    'datetime',
    'dbm',
    'decimal',
    'difflib',
    'dis',
    'distutils',
    'doctest',
    'email',
    'encodings',
    'ensurepip',
    'enum',
    'errno',
    'faulthandler',
    'fcntl',
    'filecmp',
    'fileinput',
    'fnmatch',
    'fractions',
    'ftplib',
    'functools',
    'gc',
    'genericpath',
    'getopt',
    'getpass',
    'gettext',
    'glob',
    'graphlib',
    'grp',
    'gzip',
    'hashlib',
    'heapq',
    'hmac',
    'html',
    'http',
    'imaplib',
    'imghdr',
    'imp',
    'importlib',
    'inspect',
    'io',
    'ipaddress',
    'itertools',
    'json',
    'keyword',
    'lib2to3',
    'linecache',
    'locale',
    'logging',
    'lzma',
    'mailbox',
    'mailcap',
    'marshal',
    'math',
    'mimetypes',
    'mmap',
    'modulefinder',
    'multiprocessing',
    'netrc',
    'nis',
    'nntplib',
    'ntpath',
    'nturl2path',
    'numbers',
    'opcode',
    'operator',
    'optparse',
    'os',
    'ossaudiodev',
    'pathlib',
    'pdb',
    'pickle',
    'pickletools',
    'pip',
    'pipes',
    'pkg_resources',
    'pkgutil',
    'platform',
    'plistlib',
    'poplib',
    'posix',
    'posixpath',
    'pprint',
    'profile',
    'pstats',
    'pty',
    'pwd',
    'py_compile',
    'pyclbr',
    'pydoc',
    'pydoc_data',
    'pyexpat',
    'queue',
    'quopri',
    'random',
    're',
    'readline',
    'reprlib',
    'resource',
    'rlcompleter',
    'runpy',
    'sched',
    'secrets',
    'select',
    'selectors',
    'setuptools',
    'shelve',
    'shlex',
    'shutil',
    'signal',
    'site',
    'sitecustomize',
    'smtpd',
    'smtplib',
    'sndhdr',
    'socket',
    'socketserver',
    'spwd',
    'sqlite3',
    'sre_compile',
    'sre_constants',
    'sre_parse',
    'ssl',
    'stat',
    'statistics',
    'string',
    'stringprep',
    'struct',
    'subprocess',
    'sunau',
    'symtable',
    'sys',
    'sysconfig',
    'syslog',
    'tabnanny',
    'tarfile',
    'telnetlib',
    'tempfile',
    'termios',
    'test',
    'textwrap',
    'this',
    'threading',
    'time',
    'timeit',
    'token',
    'tokenize',
    'trace',
    'traceback',
    'tracemalloc',
    'tty',
    'turtle',
    'types',
    'typing',
    'unicodedata',
    'unittest',
    'urllib',
    'uu',
    'uuid',
    'venv',
    'warnings',
    'wave',
    'weakref',
    'webbrowser',
    'wsgiref',
    'xdrlib',
    'xml',
    'xmlrpc',
    'xpto',
    'xxlimited',
    'xxlimited_35',
    'xxsubtype',
    'zipapp',
    'zipfile',
    'zipimport',
    'zlib',
    'zoneinfo',
]

BUILTIN_FUNCTIONS: Final[list[str]] = [
    'abs',
    'all',
    'any',
    'ascii',
    'bin',
    'bool',
    'bytearray',
    'bytes',
    'callable',
    'chr',
    'classmethod',
    'compile',
    'complex',
    'delattr',
    'dict',
    'dir',
    'divmod',
    'enumerate',
    'eval',
    'exec',
    'filter',
    'float',
    'format',
    'frozenset',
    'getattr',
    'globals',
    'hasattr',
    'hash',
    'help',
    'hex',
    'id',
    'input',
    'int',
    'isinstance',
    'issubclass',
    'iter',
    'len',
    'list',
    'locals',
    'map',
    'max',
    'memoryview',
    'min',
    'next',
    'object',
    'oct',
    'open',
    'ord',
    'pow',
    'print',
    'property',
    'range',
    'repr',
    'reversed',
    'round',
    'set',
    'setattr',
    'slice',
    'sorted',
    'staticmethod',
    'str',
    'sum',
    'super',
    'tuple',
    'type',
    'vars',
    'zip',
]

BUILTIN_DUNDER_METHODS: Final[list[str]] = [
    '__abs__',
    '__add__',
    '__aenter__',
    '__aexit__',
    '__aiter__',
    '__and__',
    '__anext__',
    '__await__',
    '__bool__',
    '__bytes__',
    '__call__',
    '__ceil__',
    '__class_getitem__',
    '__complex__',
    '__contains__',
    '__del__',
    '__delattr__',
    '__delete__',
    '__delitem__',
    '__dir__',
    '__divmod__',
    '__enter__',
    '__eq__',
    '__exit__',
    '__float__',
    '__floor__',
    '__floordiv__',
    '__format__',
    '__ge__',
    '__get__',
    '__getattr__',
    '__getattribute__',
    '__getitem__',
    '__gt__',
    '__hash__',
    '__iadd__',
    '__index__',
    '__init__',
    '__init_subclass__',
    '__instancecheck__',
    '__int__',
    '__invert__',
    '__iter__',
    '__le__',
    '__len__',
    '__length_hint__',
    '__lshift__',
    '__lt__',
    '__matmul__',
    '__missing__',
    '__mod__',
    '__mul__',
    '__ne__',
    '__neg__',
    '__new__',
    '__or__',
    '__pos__',
    '__pow__',
    '__radd__',
    '__repr__',
    '__reversed__',
    '__round__',
    '__rshift__',
    '__set__',
    '__set_name__',
    '__setattr__',
    '__setitem__',
    '__str__',
    '__sub__',
    '__subclasscheck__',
    '__truediv__',
    '__trunc__',
    '__xor__',
]

ACCEPTABLE_LOWER_CONSTANTS: Final[list[str]] = [
    '__author__',
    '__copyright__',
    '__credits__',
    '__date__',
    '__email__',
    '__keywords__',
    '__license__',
    '__maintainer__',
    '__repository__',
    '__status__',
    '__version__',
    'app',
    'app_name',
    'application',
    'main',
    'urlpatterns',
]

DEFAULT_MKDOCS_YML: Final[str] = """site_name: {proj_name}
repo_url: {repo_url}
repo_name: {repo_name}
edit_uri: "{edit_uri}"


theme:
  name: material
  language: en
  favicon: {logo_path}
  logo: {logo_path}
  font:
    text: Ubuntu

  icon:
    tag:
      homepage: fontawesome/solid/house
      index: fontawesome/solid/file
      overview: fontawesome/solid/binoculars
      test: fontawesome/solid/flask-vial
      infra: fontawesome/solid/server
      doc: fontawesome/solid/book
      legal: fontawesome/solid/scale-unbalanced
      user: fontawesome/solid/user
      API: fontawesome/solid/gears
      browser: fontawesome/solid/desktop

    next: fontawesome/solid/arrow-right
    previous: fontawesome/solid/arrow-left
    top: fontawesome/solid/arrow-up
    repo: fontawesome/brands/git-alt
    edit: material/pencil
    view: material/eye
    admonition:
      note: fontawesome/solid/note-sticky
      abstract: fontawesome/solid/book
      info: fontawesome/solid/circle-info
      tip: fontawesome/solid/fire-flame-simple
      success: fontawesome/solid/check
      question: fontawesome/solid/circle-question
      warning: fontawesome/solid/triangle-exclamation
      failure: fontawesome/solid/xmark
      danger: fontawesome/solid/skull
      bug: fontawesome/solid/bug
      example: fontawesome/solid/flask
      quote: fontawesome/solid/quote-left

  palette:
    # Palette toggle for light mode
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Light/Dark Mode
      primary: green
      accent: indigo

    # Palette toggle for dark mode
    - scheme: slate
      toggle:
        icon: material/brightness-3
        name: Light/Dark Mode
      primary: teal
      accent: orange


  features:
    - navigation.indexes
    - navigation.tabs
    - navigation.top
    - toc.integrate
    - header.autohide
    - navigation.footer
    - content.action.view
    - content.action.edit
    - announce.dismiss
    - content.tabs.link


markdown_extensions:
  - attr_list
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      use_pygments: true
      pygments_lang_class: true
      auto_title: true
      linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - admonition
  - pymdownx.details
  - attr_list
  - md_in_html
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.arithmatex:
      generic: true
  - def_list
  - pymdownx.tasklist:
      custom_checkbox: true
      clickable_checkbox: false


plugins:
  - search
  - tags
  - git-revision-date-localized:
      enable_creation_date: true
      type: datetime
      enabled: true
      enable_creation_date: true
      fallback_to_build_date: true
      locale: en


extra:
  tags:
    Homepage: homepage
    Index: index
    Overview: overview
    Test: test
    Infra: infra
    Documentation: doc
    Legal: legal
    Usuário: user
    API: API
    Browser: browser

  status:
    new: Recently Added!


copyright: Only God knows


"""

FILE_MARKDOWN: Final[str] = """# File: `{filename}`

Role: {role}

Path: `{filepath}`

{filedoc}

---

## Imports

{imports}

---

## Consts

{constants}

---

## Classes

{classes}

---

## Functions

{functions}

---

## Assertions

{assertions}
"""

IMPORT_MD_STRUCT: Final[str] = """### `#!py import {name}`

Path: `#!py {_path}`

Category: {category}

??? example "SNIPPET"

    ```py
{code}
    ```

"""

ASSIGN_MD_STRUCT: Final[str] = """### `#!py {token}`

Type: `#!py {_type}`

Value: `#!py {value}`

??? example "SNIPPET"

    ```py
{code}
    ```

"""

CLASS_DEF_MD_STRUCT: Final[str] = """### `#!py class {name}`

Parents: `{inherit}`

Decorators: `#!py {decorators}`

Kwargs: `#!py {kwargs}`

{docstring}

??? example "SNIPPET"

    ```py
{code}
    ```

"""

FUNCTION_DEF_MD_STRUCT: Final[str] = """### `#!py def {name}`

Type: `#!py {category}`

Return Type: `#!py {rtype}`

Decorators: `#!py {decorators}`

Args: `#!py {args}`

Kwargs: `#!py {kwargs}`

{docstring}

??? example "SNIPPET"

    ```py
{code}
    ```

"""

ASSERT_MD_STRUCT: Final[str] = """### `#!py assert {test}`

Message: `#!py {msg}`

??? example "SNIPPET"

    ```py
{code}
    ```

"""
