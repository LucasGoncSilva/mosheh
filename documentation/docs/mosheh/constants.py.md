# File: `constants.py`

Role: Python Source Code

Path: `mosheh`

This module defines constants and templates used throughout the project.

It aims to standardize project-wide values, ensure consistency, and streamline the
development and documentation process.

The constants defined here are:

1. `BUILTIN_MODULES`: A comprehensive list of Python's built-in modules for reference or
   validation purposes.

2. `BUILTIN_FUNCTIONS`: A list of Python's built-in functions to support validation,
   documentation or tooling needs.

3. `BUILTIN_DUNDER_METHODS`: Commonly used double-underscore (dunder) methods in Python,
   aiding in validation or documentation.

4. `ACCEPTABLE_LOWER_CONSTANTS`: Lowercase constants acceptable in the project to
   enforce naming conventions.

5. `DEFAULT_MKDOCS_YML`: A template for MkDocs configuration using the Material theme,
   with custom settings for a consistent and professional documentation structure.

6. Markdown Templates:
   - Files (`FILE_MARKDOWN`)
   - Imports (`IMPORT_MD_STRUCT`)
   - Assignments (`ASSIGN_MD_STRUCT`)
   - Classes (`CLASS_DEF_MD_STRUCT`)
   - Functions (`FUNCTION_DEF_MD_STRUCT`)
   - Assertions (`ASSERT_MD_STRUCT`)

These constants can be imported and reused wherever needed in the project. Be careful
when updating this file to maintain consistency across the project. Remember that this
file should remain immutable during runtime and utilize Python's `typing.Final` type
hint to mark constants as non-overridable.

---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

---

## Consts

### `#!py BUILTIN_MODULES`

Type: `#!py Final[list[str]]`

Value: `#!py ['__future__', '_abc', '_aix_support', '_ast', '_asyncio', '_bisect', '_blake2', '_bootsubprocess', '_bz2', '_codecs', '_codecs_cn', '_codecs_hk', '_codecs_iso2022', '_codecs_jp', '_codecs_kr', '_codecs_tw', '_collections', '_collections_abc', '_compat_pickle', '_compression', '_contextvars', '_crypt', '_csv', '_ctypes', '_ctypes_test', '_curses', '_curses_panel', '_datetime', '_dbm', '_decimal', '_distutils_hack', '_distutils_system_mod', '_elementtree', '_functools', '_gdbm', '_hashlib', '_heapq', '_imp', '_io', '_json', '_locale', '_lsprof', '_lzma', '_markupbase', '_md5', '_multibytecodec', '_multiprocessing', '_opcode', '_operator', '_osx_support', '_pickle', '_posixshmem', '_posixsubprocess', '_py_abc', '_pydecimal', '_pyio', '_queue', '_random', '_sha1', '_sha256', '_sha3', '_sha512', '_signal', '_sitebuiltins', '_socket', '_sqlite3', '_sre', '_ssl', '_stat', '_statistics', '_string', '_strptime', '_struct', '_symtable', '_sysconfigdata__linux_x86_64-linux-gnu', '_sysconfigdata__x86_64-linux-gnu', '_testbuffer', '_testcapi', '_testclinic', '_testimportmultiple', '_testinternalcapi', '_testmultiphase', '_thread', '_threading_local', '_tracemalloc', '_uuid', '_warnings', '_weakref', '_weakrefset', '_xxsubinterpreters', '_xxtestfuzz', '_zoneinfo', 'abc', 'aifc', 'antigravity', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'cProfile', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'fractions', 'ftplib', 'functools', 'gc', 'genericpath', 'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'ntpath', 'nturl2path', 'numbers', 'opcode', 'operator', 'optparse', 'os', 'ossaudiodev', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pip', 'pipes', 'pkg_resources', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'pydoc_data', 'pyexpat', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'setuptools', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'sitecustomize', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'sre_compile', 'sre_constants', 'sre_parse', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'this', 'threading', 'time', 'timeit', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'xpto', 'xxlimited', 'xxlimited_35', 'xxsubtype', 'zipapp', 'zipfile', 'zipimport', 'zlib', 'zoneinfo']`

??? example "SNIPPET"

    ```py
    BUILTIN_MODULES: Final[list[str]] = ['__future__', '_abc', '_aix_support', '_ast', '_asyncio', '_bisect', '_blake2', '_bootsubprocess', '_bz2', '_codecs', '_codecs_cn', '_codecs_hk', '_codecs_iso2022', '_codecs_jp', '_codecs_kr', '_codecs_tw', '_collections', '_collections_abc', '_compat_pickle', '_compression', '_contextvars', '_crypt', '_csv', '_ctypes', '_ctypes_test', '_curses', '_curses_panel', '_datetime', '_dbm', '_decimal', '_distutils_hack', '_distutils_system_mod', '_elementtree', '_functools', '_gdbm', '_hashlib', '_heapq', '_imp', '_io', '_json', '_locale', '_lsprof', '_lzma', '_markupbase', '_md5', '_multibytecodec', '_multiprocessing', '_opcode', '_operator', '_osx_support', '_pickle', '_posixshmem', '_posixsubprocess', '_py_abc', '_pydecimal', '_pyio', '_queue', '_random', '_sha1', '_sha256', '_sha3', '_sha512', '_signal', '_sitebuiltins', '_socket', '_sqlite3', '_sre', '_ssl', '_stat', '_statistics', '_string', '_strptime', '_struct', '_symtable', '_sysconfigdata__linux_x86_64-linux-gnu', '_sysconfigdata__x86_64-linux-gnu', '_testbuffer', '_testcapi', '_testclinic', '_testimportmultiple', '_testinternalcapi', '_testmultiphase', '_thread', '_threading_local', '_tracemalloc', '_uuid', '_warnings', '_weakref', '_weakrefset', '_xxsubinterpreters', '_xxtestfuzz', '_zoneinfo', 'abc', 'aifc', 'antigravity', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'cProfile', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'fractions', 'ftplib', 'functools', 'gc', 'genericpath', 'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'ntpath', 'nturl2path', 'numbers', 'opcode', 'operator', 'optparse', 'os', 'ossaudiodev', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pip', 'pipes', 'pkg_resources', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'pydoc_data', 'pyexpat', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'setuptools', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'sitecustomize', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'sre_compile', 'sre_constants', 'sre_parse', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'this', 'threading', 'time', 'timeit', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'xpto', 'xxlimited', 'xxlimited_35', 'xxsubtype', 'zipapp', 'zipfile', 'zipimport', 'zlib', 'zoneinfo']
    ```

### `#!py BUILTIN_FUNCTIONS`

Type: `#!py Final[list[str]]`

Value: `#!py ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']`

??? example "SNIPPET"

    ```py
    BUILTIN_FUNCTIONS: Final[list[str]] = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
    ```

### `#!py BUILTIN_DUNDER_METHODS`

Type: `#!py Final[list[str]]`

Value: `#!py ['__abs__', '__add__', '__aenter__', '__aexit__', '__aiter__', '__and__', '__anext__', '__await__', '__bool__', '__bytes__', '__call__', '__ceil__', '__class_getitem__', '__complex__', '__contains__', '__del__', '__delattr__', '__delete__', '__delitem__', '__dir__', '__divmod__', '__enter__', '__eq__', '__exit__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__get__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__index__', '__init__', '__init_subclass__', '__instancecheck__', '__int__', '__invert__', '__iter__', '__le__', '__len__', '__length_hint__', '__lshift__', '__lt__', '__matmul__', '__missing__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__repr__', '__reversed__', '__round__', '__rshift__', '__set__', '__set_name__', '__setattr__', '__setitem__', '__str__', '__sub__', '__subclasscheck__', '__truediv__', '__trunc__', '__xor__']`

??? example "SNIPPET"

    ```py
    BUILTIN_DUNDER_METHODS: Final[list[str]] = ['__abs__', '__add__', '__aenter__', '__aexit__', '__aiter__', '__and__', '__anext__', '__await__', '__bool__', '__bytes__', '__call__', '__ceil__', '__class_getitem__', '__complex__', '__contains__', '__del__', '__delattr__', '__delete__', '__delitem__', '__dir__', '__divmod__', '__enter__', '__eq__', '__exit__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__get__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__index__', '__init__', '__init_subclass__', '__instancecheck__', '__int__', '__invert__', '__iter__', '__le__', '__len__', '__length_hint__', '__lshift__', '__lt__', '__matmul__', '__missing__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__repr__', '__reversed__', '__round__', '__rshift__', '__set__', '__set_name__', '__setattr__', '__setitem__', '__str__', '__sub__', '__subclasscheck__', '__truediv__', '__trunc__', '__xor__']
    ```

### `#!py ACCEPTABLE_LOWER_CONSTANTS`

Type: `#!py Final[list[str]]`

Value: `#!py ['__author__', '__copyright__', '__credits__', '__date__', '__email__', '__keywords__', '__license__', '__maintainer__', '__repository__', '__status__', '__version__', 'app', 'app_name', 'application', 'main', 'urlpatterns']`

??? example "SNIPPET"

    ```py
    ACCEPTABLE_LOWER_CONSTANTS: Final[list[str]] = ['__author__', '__copyright__', '__credits__', '__date__', '__email__', '__keywords__', '__license__', '__maintainer__', '__repository__', '__status__', '__version__', 'app', 'app_name', 'application', 'main', 'urlpatterns']
    ```

### `#!py DEFAULT_MKDOCS_YML`

Type: `#!py Final[str]`

Value: `#!py 'site_name: {proj_name}\nrepo_url: {repo_url}\nrepo_name: {repo_name}\nedit_uri: "{edit_uri}"\n\n\ntheme:\n  name: material\n  language: en\n  favicon: {logo_path}\n  logo: {logo_path}\n  font:\n    text: Ubuntu\n\n  icon:\n    tag:\n      homepage: fontawesome/solid/house\n      index: fontawesome/solid/file\n      overview: fontawesome/solid/binoculars\n      test: fontawesome/solid/flask-vial\n      infra: fontawesome/solid/server\n      doc: fontawesome/solid/book\n      legal: fontawesome/solid/scale-unbalanced\n      user: fontawesome/solid/user\n      API: fontawesome/solid/gears\n      browser: fontawesome/solid/desktop\n\n    next: fontawesome/solid/arrow-right\n    previous: fontawesome/solid/arrow-left\n    top: fontawesome/solid/arrow-up\n    repo: fontawesome/brands/git-alt\n    edit: material/pencil\n    view: material/eye\n    admonition:\n      note: fontawesome/solid/note-sticky\n      abstract: fontawesome/solid/book\n      info: fontawesome/solid/circle-info\n      tip: fontawesome/solid/fire-flame-simple\n      success: fontawesome/solid/check\n      question: fontawesome/solid/circle-question\n      warning: fontawesome/solid/triangle-exclamation\n      failure: fontawesome/solid/xmark\n      danger: fontawesome/solid/skull\n      bug: fontawesome/solid/bug\n      example: fontawesome/solid/flask\n      quote: fontawesome/solid/quote-left\n\n  palette:\n    # Palette toggle for light mode\n    - scheme: default\n      toggle:\n        icon: material/brightness-7\n        name: Light/Dark Mode\n      primary: green\n      accent: indigo\n\n    # Palette toggle for dark mode\n    - scheme: slate\n      toggle:\n        icon: material/brightness-3\n        name: Light/Dark Mode\n      primary: teal\n      accent: orange\n\n\n  features:\n    - navigation.indexes\n    - navigation.tabs\n    - navigation.top\n    - toc.integrate\n    - header.autohide\n    - navigation.footer\n    - content.action.view\n    - content.action.edit\n    - announce.dismiss\n    - content.tabs.link\n\n\nmarkdown_extensions:\n  - attr_list\n  - pymdownx.emoji:\n      emoji_index: !!python/name:material.extensions.emoji.twemoji\n      emoji_generator: !!python/name:material.extensions.emoji.to_svg\n  - pymdownx.highlight:\n      anchor_linenums: true\n      use_pygments: true\n      pygments_lang_class: true\n      auto_title: true\n      linenums: true\n  - pymdownx.inlinehilite\n  - pymdownx.snippets\n  - pymdownx.superfences:\n      custom_fences:\n        - name: mermaid\n          class: mermaid\n          format: !!python/name:pymdownx.superfences.fence_code_format\n  - admonition\n  - pymdownx.details\n  - attr_list\n  - md_in_html\n  - pymdownx.tabbed:\n      alternate_style: true\n  - pymdownx.arithmatex:\n      generic: true\n  - def_list\n  - pymdownx.tasklist:\n      custom_checkbox: true\n      clickable_checkbox: false\n\n\nplugins:\n  - search\n  - tags\n  - git-revision-date-localized:\n      enable_creation_date: true\n      type: datetime\n      enabled: true\n      enable_creation_date: true\n      fallback_to_build_date: true\n      locale: en\n\n\nextra:\n  tags:\n    Homepage: homepage\n    Index: index\n    Overview: overview\n    Test: test\n    Infra: infra\n    Documentation: doc\n    Legal: legal\n    Usuário: user\n    API: API\n    Browser: browser\n\n  status:\n    new: Recently Added!\n\n\ncopyright: Only God knows\n\n\n'`

??? example "SNIPPET"

    ```py
    DEFAULT_MKDOCS_YML: Final[str] = 'site_name: {proj_name}\nrepo_url: {repo_url}\nrepo_name: {repo_name}\nedit_uri: "{edit_uri}"\n\n\ntheme:\n  name: material\n  language: en\n  favicon: {logo_path}\n  logo: {logo_path}\n  font:\n    text: Ubuntu\n\n  icon:\n    tag:\n      homepage: fontawesome/solid/house\n      index: fontawesome/solid/file\n      overview: fontawesome/solid/binoculars\n      test: fontawesome/solid/flask-vial\n      infra: fontawesome/solid/server\n      doc: fontawesome/solid/book\n      legal: fontawesome/solid/scale-unbalanced\n      user: fontawesome/solid/user\n      API: fontawesome/solid/gears\n      browser: fontawesome/solid/desktop\n\n    next: fontawesome/solid/arrow-right\n    previous: fontawesome/solid/arrow-left\n    top: fontawesome/solid/arrow-up\n    repo: fontawesome/brands/git-alt\n    edit: material/pencil\n    view: material/eye\n    admonition:\n      note: fontawesome/solid/note-sticky\n      abstract: fontawesome/solid/book\n      info: fontawesome/solid/circle-info\n      tip: fontawesome/solid/fire-flame-simple\n      success: fontawesome/solid/check\n      question: fontawesome/solid/circle-question\n      warning: fontawesome/solid/triangle-exclamation\n      failure: fontawesome/solid/xmark\n      danger: fontawesome/solid/skull\n      bug: fontawesome/solid/bug\n      example: fontawesome/solid/flask\n      quote: fontawesome/solid/quote-left\n\n  palette:\n    # Palette toggle for light mode\n    - scheme: default\n      toggle:\n        icon: material/brightness-7\n        name: Light/Dark Mode\n      primary: green\n      accent: indigo\n\n    # Palette toggle for dark mode\n    - scheme: slate\n      toggle:\n        icon: material/brightness-3\n        name: Light/Dark Mode\n      primary: teal\n      accent: orange\n\n\n  features:\n    - navigation.indexes\n    - navigation.tabs\n    - navigation.top\n    - toc.integrate\n    - header.autohide\n    - navigation.footer\n    - content.action.view\n    - content.action.edit\n    - announce.dismiss\n    - content.tabs.link\n\n\nmarkdown_extensions:\n  - attr_list\n  - pymdownx.emoji:\n      emoji_index: !!python/name:material.extensions.emoji.twemoji\n      emoji_generator: !!python/name:material.extensions.emoji.to_svg\n  - pymdownx.highlight:\n      anchor_linenums: true\n      use_pygments: true\n      pygments_lang_class: true\n      auto_title: true\n      linenums: true\n  - pymdownx.inlinehilite\n  - pymdownx.snippets\n  - pymdownx.superfences:\n      custom_fences:\n        - name: mermaid\n          class: mermaid\n          format: !!python/name:pymdownx.superfences.fence_code_format\n  - admonition\n  - pymdownx.details\n  - attr_list\n  - md_in_html\n  - pymdownx.tabbed:\n      alternate_style: true\n  - pymdownx.arithmatex:\n      generic: true\n  - def_list\n  - pymdownx.tasklist:\n      custom_checkbox: true\n      clickable_checkbox: false\n\n\nplugins:\n  - search\n  - tags\n  - git-revision-date-localized:\n      enable_creation_date: true\n      type: datetime\n      enabled: true\n      enable_creation_date: true\n      fallback_to_build_date: true\n      locale: en\n\n\nextra:\n  tags:\n    Homepage: homepage\n    Index: index\n    Overview: overview\n    Test: test\n    Infra: infra\n    Documentation: doc\n    Legal: legal\n    Usuário: user\n    API: API\n    Browser: browser\n\n  status:\n    new: Recently Added!\n\n\ncopyright: Only God knows\n\n\n'
    ```

### `#!py FILE_MARKDOWN`

Type: `#!py Final[str]`

Value: `#!py '# File: `{filename}`\n\nRole: {role}\n\nPath: `{filepath}`\n\n{filedoc}\n\n---\n\n## Imports\n\n{imports}\n\n---\n\n## Consts\n\n{constants}\n\n---\n\n## Classes\n\n{classes}\n\n---\n\n## Functions\n\n{functions}\n\n---\n\n## Assertions\n\n{assertions}\n'`

??? example "SNIPPET"

    ```py
    FILE_MARKDOWN: Final[str] = '# File: `{filename}`\n\nRole: {role}\n\nPath: `{filepath}`\n\n{filedoc}\n\n---\n\n## Imports\n\n{imports}\n\n---\n\n## Consts\n\n{constants}\n\n---\n\n## Classes\n\n{classes}\n\n---\n\n## Functions\n\n{functions}\n\n---\n\n## Assertions\n\n{assertions}\n'
    ```

### `#!py IMPORT_MD_STRUCT`

Type: `#!py Final[str]`

Value: `#!py '### `#!py import {name}`\n\nPath: `#!py {\_path}` \n\nCategory: {category}\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n' `

??? example "SNIPPET"

    ```py
    IMPORT_MD_STRUCT: Final[str] = '### `#!py import {name}`\n\nPath: `#!py {_path}`\n\nCategory: {category}\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n'
    ```

### `#!py ASSIGN_MD_STRUCT`

Type: `#!py Final[str]`

Value: `#!py '### `#!py {token}`\n\nType: `#!py {\_type}`\n\nValue: `#!py {value}` \n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n' `

??? example "SNIPPET"

    ```py
    ASSIGN_MD_STRUCT: Final[str] = '### `#!py {token}`\n\nType: `#!py {_type}`\n\nValue: `#!py {value}`\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n'
    ```

### `#!py CLASS_DEF_MD_STRUCT`

Type: `#!py Final[str]`

Value: `#!py '### `#!py class {name}`\n\nParents: `{inherit}`\n\nDecorators: `#!py {decorators}`\n\nKwargs: `#!py {kwargs}` \n\n{docstring}\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n' `

??? example "SNIPPET"

    ```py
    CLASS_DEF_MD_STRUCT: Final[str] = '### `#!py class {name}`\n\nParents: `{inherit}`\n\nDecorators: `#!py {decorators}`\n\nKwargs: `#!py {kwargs}`\n\n{docstring}\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n'
    ```

### `#!py FUNCTION_DEF_MD_STRUCT`

Type: `#!py Final[str]`

Value: `#!py '### `#!py def {name}`\n\nType: `#!py {category}`\n\nReturn Type: `#!py {rtype}`\n\nDecorators: `#!py {decorators}`\n\nArgs: `#!py {args}`\n\nKwargs: `#!py {kwargs}` \n\n{docstring}\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n' `

??? example "SNIPPET"

    ```py
    FUNCTION_DEF_MD_STRUCT: Final[str] = '### `#!py def {name}`\n\nType: `#!py {category}`\n\nReturn Type: `#!py {rtype}`\n\nDecorators: `#!py {decorators}`\n\nArgs: `#!py {args}`\n\nKwargs: `#!py {kwargs}`\n\n{docstring}\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n'
    ```

### `#!py ASSERT_MD_STRUCT`

Type: `#!py Final[str]`

Value: `#!py '### `#!py assert {test}`\n\nMessage: `#!py {msg}` \n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n' `

??? example "SNIPPET"

    ```py
    ASSERT_MD_STRUCT: Final[str] = '### `#!py assert {test}`\n\nMessage: `#!py {msg}`\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n'
    ```

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

!!! info "NO FUNCTION DEFINED HERE"

---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
