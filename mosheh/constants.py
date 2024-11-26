from typing import Final


__BUILTIN_MODULES: Final[list[str]] = [
    '__future__',
    '_testclinic',
    'getopt',
    'runpy',
    '_abc',
    '_testimportmultiple',
    'getpass',
    'sched',
    '_aix_support',
    '_testinternalcapi',
    'gettext',
    'secrets',
    '_ast',
    '_testmultiphase',
    'glob',
    'select',
    '_asyncio',
    '_thread',
    'graphlib',
    'selectors',
    '_bisect',
    '_threading_local',
    'grp',
    'setuptools',
    '_blake2',
    '_tracemalloc',
    'gzip',
    'shelve',
    '_bootsubprocess',
    '_uuid',
    'hashlib',
    'shlex',
    '_bz2',
    '_warnings',
    'heapq',
    'shutil',
    '_codecs',
    '_weakref',
    'hmac',
    'signal',
    '_codecs_cn',
    '_weakrefset',
    'html',
    'site',
    '_codecs_hk',
    '_xxsubinterpreters',
    'http',
    'sitecustomize',
    '_codecs_iso2022',
    '_xxtestfuzz',
    'imaplib',
    'smtpd',
    '_codecs_jp',
    '_zoneinfo',
    'imghdr',
    'smtplib',
    '_codecs_kr',
    'abc',
    'imp',
    'sndhdr',
    '_codecs_tw',
    'aifc',
    'importlib',
    'socket',
    '_collections',
    'antigravity',
    'inspect',
    'socketserver',
    '_collections_abc',
    'argparse',
    'io',
    'spwd',
    '_compat_pickle',
    'array',
    'ipaddress',
    'sqlite3',
    '_compression',
    'ast',
    'itertools',
    'sre_compile',
    '_contextvars',
    'asynchat',
    'json',
    'sre_constants',
    '_crypt',
    'asyncio',
    'keyword',
    'sre_parse',
    '_csv',
    'asyncore',
    'lib2to3',
    'ssl',
    '_ctypes',
    'atexit',
    'linecache',
    'stat',
    '_ctypes_test',
    'audioop',
    'locale',
    'statistics',
    '_curses',
    'base64',
    'logging',
    'string',
    '_curses_panel',
    'bdb',
    'lzma',
    'stringprep',
    '_datetime',
    'binascii',
    'mailbox',
    'struct',
    '_dbm',
    'binhex',
    'mailcap',
    'subprocess',
    '_decimal',
    'bisect',
    'marshal',
    'sunau',
    '_distutils_hack',
    'builtins',
    'math',
    'symtable',
    '_distutils_system_mod',
    'bz2',
    'mimetypes',
    'sys',
    '_elementtree',
    'cProfile',
    'mmap',
    'sysconfig',
    '_functools',
    'calendar',
    'modulefinder',
    'syslog',
    '_gdbm',
    'cgi',
    'multiprocessing',
    'tabnanny',
    '_hashlib',
    'cgitb',
    'netrc',
    'tarfile',
    '_heapq',
    'chunk',
    'nis',
    'telnetlib',
    '_imp',
    'cmath',
    'nntplib',
    'tempfile',
    '_io',
    'cmd',
    'ntpath',
    'termios',
    '_json',
    'code',
    'nturl2path',
    'test',
    '_locale',
    'codecs',
    'numbers',
    'textwrap',
    '_lsprof',
    'codeop',
    'opcode',
    'this',
    '_lzma',
    'collections',
    'operator',
    'threading',
    '_markupbase',
    'colorsys',
    'optparse',
    'time',
    '_md5',
    'compileall',
    'os',
    'timeit',
    '_multibytecodec',
    'concurrent',
    'ossaudiodev',
    'token',
    '_multiprocessing',
    'configparser',
    'pathlib',
    'tokenize',
    '_opcode',
    'contextlib',
    'pdb',
    'trace',
    '_operator',
    'contextvars',
    'pickle',
    'traceback',
    '_osx_support',
    'copy',
    'pickletools',
    'tracemalloc',
    '_pickle',
    'copyreg',
    'pip',
    'tty',
    '_posixshmem',
    'crypt',
    'pipes',
    'turtle',
    '_posixsubprocess',
    'csv',
    'pkg_resources',
    'types',
    '_py_abc',
    'ctypes',
    'pkgutil',
    'typing',
    '_pydecimal',
    'curses',
    'platform',
    'unicodedata',
    '_pyio',
    'dataclasses',
    'plistlib',
    'unittest',
    '_queue',
    'datetime',
    'poplib',
    'urllib',
    '_random',
    'dbm',
    'posix',
    'uu',
    '_sha1',
    'decimal',
    'posixpath',
    'uuid',
    '_sha256',
    'difflib',
    'pprint',
    'venv',
    '_sha3',
    'dis',
    'profile',
    'warnings',
    '_sha512',
    'distutils',
    'pstats',
    'wave',
    '_signal',
    'doctest',
    'pty',
    'weakref',
    '_sitebuiltins',
    'email',
    'pwd',
    'webbrowser',
    '_socket',
    'encodings',
    'py_compile',
    'wsgiref',
    '_sqlite3',
    'ensurepip',
    'pyclbr',
    'xdrlib',
    '_sre',
    'enum',
    'pydoc',
    'xml',
    '_ssl',
    'errno',
    'pydoc_data',
    'xmlrpc',
    '_stat',
    'faulthandler',
    'pyexpat',
    'xpto',
    '_statistics',
    'fcntl',
    'queue',
    'xxlimited',
    '_string',
    'filecmp',
    'quopri',
    'xxlimited_35',
    '_strptime',
    'fileinput',
    'random',
    'xxsubtype',
    '_struct',
    'fnmatch',
    're',
    'zipapp',
    '_symtable',
    'fractions',
    'readline',
    'zipfile',
    '_sysconfigdata__linux_x86_64-linux-gnu',
    'ftplib',
    'reprlib',
    'zipimport',
    '_sysconfigdata__x86_64-linux-gnu',
    'functools',
    'resource',
    'zlib',
    '_testbuffer',
    'gc',
    'rlcompleter',
    'zoneinfo',
    '_testcapi',
    'genericpath',
]

__BUILTIN_FUNCTIONS: Final[list[str]] = [
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

__BUILTIN_DUNDER_METHODS: Final[list[str]] = [
    '__init__',
    '__new__',
    '__del__',
    '__repr__',
    '__str__',
    '__bytes__',
    '__format__',
    '__lt__',
    '__le__',
    '__eq__',
    '__ne__',
    '__gt__',
    '__ge__',
    '__hash__',
    '__bool__',
    '__getattr__',
    '__getattribute__',
    '__setattr__',
    '__delattr__',
    '__dir__',
    '__get__',
    '__set__',
    '__delete__',
    '__init_subclass__',
    '__set_name__',
    '__instancecheck__',
    '__subclasscheck__',
    '__class_getitem__',
    '__call__',
    '__len__',
    '__length_hint__',
    '__getitem__',
    '__setitem__',
    '__delitem__',
    '__missing__',
    '__iter__',
    '__reversed__',
    '__contains__',
    '__add__',
    '__radd__',
    '__iadd__',
    '__sub__',
    '__mul__',
    '__matmul__',
    '__truediv__',
    '__floordiv__',
    '__mod__',
    '__divmod__',
    '__pow__',
    '__lshift__',
    '__rshift__',
    '__and__',
    '__xor__',
    '__or__',
    '__neg__',
    '__pos__',
    '__abs__',
    '__invert__',
    '__complex__',
    '__int__',
    '__float__',
    '__index__',
    '__round__',
    '__trunc__',
    '__floor__',
    '__ceil__',
    '__enter__',
    '__exit__',
    '__await__',
    '__aiter__',
    '__anext__',
    '__aenter__',
    '__aexit__',
]

BUILTIN_MODULES: Final[list[str]] = list(sorted(__BUILTIN_MODULES))
BUILTIN_FUNCTIONS: Final[list[str]] = list(sorted(__BUILTIN_FUNCTIONS))
BUILTIN_DUNDER_METHODS: Final[list[str]] = list(sorted(__BUILTIN_DUNDER_METHODS))

ACCEPTABLE_LOWER_CONSTANTS: Final[list[str]] = [
    'app',
    'application',
    'urlpatterns',
    'app_name',
    'main',
]

DEFAULT_MKDOCS_YML: Final[str] = """site_name: {proj_name} | Documentation
repo_url: {repo_url}
repo_name: {repo_name}
edit_uri: "{edit_uri}"


theme:
  name: material
  language: {lang}
  # TODO: favicon: fontawesome/solid/book-open
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
  
    logo: fontawesome/solid/book-open
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
    # Palette toggle for dark mode
    - scheme: slate
      toggle:
        icon: material/brightness-3
        name: Light/Dark Mode
      primary: deep purple
      accent: deep purple

    # Palette toggle for light mode
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Light/Dark Mode
      primary: deep purple
      accent: deep purple

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
      clickable_checkbox: true


plugins:
  - search
  - tags
  - git-revision-date-localized:
      enable_creation_date: true
      type: datetime
      enabled: true
      enable_creation_date: true
      fallback_to_build_date: true
      locale: pt  # TODO automate this


extra:
  tags:
    Homepage: homepage
    Index: index
    Overview: overview
    Teste: test
    Infra: infra
    Documentation: doc
    Legal: legal
    Usuário: user
    API: API
    Browser: browser

  status:
    new: Adicionado recentemente


copyright: Only God knows


"""

FILE_MARKDOWN: Final[str] = """
# `{filename}`
`{filepath}`

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

IMPORT_MD_STRUCT: Final[str] = """### `{name}`

Path: `#!py {_path}`

Category: {category}

??? example "SNIPPET"

    ```py
{code}
    ```

"""

ASSIGN_MD_STRUCT: Final[str] = """### `{token}`

Type: `#!py {_type}`

Value: `#!py {value}`

??? example "SNIPPET"

    ```py
{code}
    ```

"""

CLASS_DEF_MD_STRUCT: Final[str] = """### `{name}`

Parents: `{inherit}`

Decorators: `#!py {decorators}`

Kwargs: {kwargs}

??? example "SNIPPET"

    ```py
{code}
    ```

"""

FUNCTION_DEF_MD_STRUCT: Final[str] = """### `{name}`

Type: `#!py ...`

Return Type: {rtype}

Decorators: `#!py {decorators}`

Args: {args}

Kwargs: {kwargs}

??? example "SNIPPET"

    ```py
{code}
    ```

"""

ASSERT_MD_STRUCT: Final[str] = """### `{test}`

Message: `#!py {msg}`

??? example "SNIPPET"

    ```py
{code}
    ```

"""
