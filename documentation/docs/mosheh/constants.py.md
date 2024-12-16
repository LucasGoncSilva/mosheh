# File: `constants.py`

Path: `mosheh`

---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import Iterable`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Iterable
    ```

---

## Consts

### `#!py BUILTIN_MODULES`

Type: `#!py Final[Iterable[str]]`

Value: `#!py sorted(['__future__', '_testclinic', 'getopt', 'runpy', '_abc', '_testimportmultiple', 'getpass', 'sched', '_aix_support', '_testinternalcapi', 'gettext', 'secrets', '_ast', '_testmultiphase', 'glob', 'select', '_asyncio', '_thread', 'graphlib', 'selectors', '_bisect', '_threading_local', 'grp', 'setuptools', '_blake2', '_tracemalloc', 'gzip', 'shelve', '_bootsubprocess', '_uuid', 'hashlib', 'shlex', '_bz2', '_warnings', 'heapq', 'shutil', '_codecs', '_weakref', 'hmac', 'signal', '_codecs_cn', '_weakrefset', 'html', 'site', '_codecs_hk', '_xxsubinterpreters', 'http', 'sitecustomize', '_codecs_iso2022', '_xxtestfuzz', 'imaplib', 'smtpd', '_codecs_jp', '_zoneinfo', 'imghdr', 'smtplib', '_codecs_kr', 'abc', 'imp', 'sndhdr', '_codecs_tw', 'aifc', 'importlib', 'socket', '_collections', 'antigravity', 'inspect', 'socketserver', '_collections_abc', 'argparse', 'io', 'spwd', '_compat_pickle', 'array', 'ipaddress', 'sqlite3', '_compression', 'ast', 'itertools', 'sre_compile', '_contextvars', 'asynchat', 'json', 'sre_constants', '_crypt', 'asyncio', 'keyword', 'sre_parse', '_csv', 'asyncore', 'lib2to3', 'ssl', '_ctypes', 'atexit', 'linecache', 'stat', '_ctypes_test', 'audioop', 'locale', 'statistics', '_curses', 'base64', 'logging', 'string', '_curses_panel', 'bdb', 'lzma', 'stringprep', '_datetime', 'binascii', 'mailbox', 'struct', '_dbm', 'binhex', 'mailcap', 'subprocess', '_decimal', 'bisect', 'marshal', 'sunau', '_distutils_hack', 'builtins', 'math', 'symtable', '_distutils_system_mod', 'bz2', 'mimetypes', 'sys', '_elementtree', 'cProfile', 'mmap', 'sysconfig', '_functools', 'calendar', 'modulefinder', 'syslog', '_gdbm', 'cgi', 'multiprocessing', 'tabnanny', '_hashlib', 'cgitb', 'netrc', 'tarfile', '_heapq', 'chunk', 'nis', 'telnetlib', '_imp', 'cmath', 'nntplib', 'tempfile', '_io', 'cmd', 'ntpath', 'termios', '_json', 'code', 'nturl2path', 'test', '_locale', 'codecs', 'numbers', 'textwrap', '_lsprof', 'codeop', 'opcode', 'this', '_lzma', 'collections', 'operator', 'threading', '_markupbase', 'colorsys', 'optparse', 'time', '_md5', 'compileall', 'os', 'timeit', '_multibytecodec', 'concurrent', 'ossaudiodev', 'token', '_multiprocessing', 'configparser', 'pathlib', 'tokenize', '_opcode', 'contextlib', 'pdb', 'trace', '_operator', 'contextvars', 'pickle', 'traceback', '_osx_support', 'copy', 'pickletools', 'tracemalloc', '_pickle', 'copyreg', 'pip', 'tty', '_posixshmem', 'crypt', 'pipes', 'turtle', '_posixsubprocess', 'csv', 'pkg_resources', 'types', '_py_abc', 'ctypes', 'pkgutil', 'typing', '_pydecimal', 'curses', 'platform', 'unicodedata', '_pyio', 'dataclasses', 'plistlib', 'unittest', '_queue', 'datetime', 'poplib', 'urllib', '_random', 'dbm', 'posix', 'uu', '_sha1', 'decimal', 'posixpath', 'uuid', '_sha256', 'difflib', 'pprint', 'venv', '_sha3', 'dis', 'profile', 'warnings', '_sha512', 'distutils', 'pstats', 'wave', '_signal', 'doctest', 'pty', 'weakref', '_sitebuiltins', 'email', 'pwd', 'webbrowser', '_socket', 'encodings', 'py_compile', 'wsgiref', '_sqlite3', 'ensurepip', 'pyclbr', 'xdrlib', '_sre', 'enum', 'pydoc', 'xml', '_ssl', 'errno', 'pydoc_data', 'xmlrpc', '_stat', 'faulthandler', 'pyexpat', 'xpto', '_statistics', 'fcntl', 'queue', 'xxlimited', '_string', 'filecmp', 'quopri', 'xxlimited_35', '_strptime', 'fileinput', 'random', 'xxsubtype', '_struct', 'fnmatch', 're', 'zipapp', '_symtable', 'fractions', 'readline', 'zipfile', '_sysconfigdata__linux_x86_64-linux-gnu', 'ftplib', 'reprlib', 'zipimport', '_sysconfigdata__x86_64-linux-gnu', 'functools', 'resource', 'zlib', '_testbuffer', 'gc', 'rlcompleter', 'zoneinfo', '_testcapi', 'genericpath'])`

??? example "SNIPPET"

    ```py
    BUILTIN_MODULES: Final[Iterable[str]] = sorted(['__future__', '_testclinic', 'getopt', 'runpy', '_abc', '_testimportmultiple', 'getpass', 'sched', '_aix_support', '_testinternalcapi', 'gettext', 'secrets', '_ast', '_testmultiphase', 'glob', 'select', '_asyncio', '_thread', 'graphlib', 'selectors', '_bisect', '_threading_local', 'grp', 'setuptools', '_blake2', '_tracemalloc', 'gzip', 'shelve', '_bootsubprocess', '_uuid', 'hashlib', 'shlex', '_bz2', '_warnings', 'heapq', 'shutil', '_codecs', '_weakref', 'hmac', 'signal', '_codecs_cn', '_weakrefset', 'html', 'site', '_codecs_hk', '_xxsubinterpreters', 'http', 'sitecustomize', '_codecs_iso2022', '_xxtestfuzz', 'imaplib', 'smtpd', '_codecs_jp', '_zoneinfo', 'imghdr', 'smtplib', '_codecs_kr', 'abc', 'imp', 'sndhdr', '_codecs_tw', 'aifc', 'importlib', 'socket', '_collections', 'antigravity', 'inspect', 'socketserver', '_collections_abc', 'argparse', 'io', 'spwd', '_compat_pickle', 'array', 'ipaddress', 'sqlite3', '_compression', 'ast', 'itertools', 'sre_compile', '_contextvars', 'asynchat', 'json', 'sre_constants', '_crypt', 'asyncio', 'keyword', 'sre_parse', '_csv', 'asyncore', 'lib2to3', 'ssl', '_ctypes', 'atexit', 'linecache', 'stat', '_ctypes_test', 'audioop', 'locale', 'statistics', '_curses', 'base64', 'logging', 'string', '_curses_panel', 'bdb', 'lzma', 'stringprep', '_datetime', 'binascii', 'mailbox', 'struct', '_dbm', 'binhex', 'mailcap', 'subprocess', '_decimal', 'bisect', 'marshal', 'sunau', '_distutils_hack', 'builtins', 'math', 'symtable', '_distutils_system_mod', 'bz2', 'mimetypes', 'sys', '_elementtree', 'cProfile', 'mmap', 'sysconfig', '_functools', 'calendar', 'modulefinder', 'syslog', '_gdbm', 'cgi', 'multiprocessing', 'tabnanny', '_hashlib', 'cgitb', 'netrc', 'tarfile', '_heapq', 'chunk', 'nis', 'telnetlib', '_imp', 'cmath', 'nntplib', 'tempfile', '_io', 'cmd', 'ntpath', 'termios', '_json', 'code', 'nturl2path', 'test', '_locale', 'codecs', 'numbers', 'textwrap', '_lsprof', 'codeop', 'opcode', 'this', '_lzma', 'collections', 'operator', 'threading', '_markupbase', 'colorsys', 'optparse', 'time', '_md5', 'compileall', 'os', 'timeit', '_multibytecodec', 'concurrent', 'ossaudiodev', 'token', '_multiprocessing', 'configparser', 'pathlib', 'tokenize', '_opcode', 'contextlib', 'pdb', 'trace', '_operator', 'contextvars', 'pickle', 'traceback', '_osx_support', 'copy', 'pickletools', 'tracemalloc', '_pickle', 'copyreg', 'pip', 'tty', '_posixshmem', 'crypt', 'pipes', 'turtle', '_posixsubprocess', 'csv', 'pkg_resources', 'types', '_py_abc', 'ctypes', 'pkgutil', 'typing', '_pydecimal', 'curses', 'platform', 'unicodedata', '_pyio', 'dataclasses', 'plistlib', 'unittest', '_queue', 'datetime', 'poplib', 'urllib', '_random', 'dbm', 'posix', 'uu', '_sha1', 'decimal', 'posixpath', 'uuid', '_sha256', 'difflib', 'pprint', 'venv', '_sha3', 'dis', 'profile', 'warnings', '_sha512', 'distutils', 'pstats', 'wave', '_signal', 'doctest', 'pty', 'weakref', '_sitebuiltins', 'email', 'pwd', 'webbrowser', '_socket', 'encodings', 'py_compile', 'wsgiref', '_sqlite3', 'ensurepip', 'pyclbr', 'xdrlib', '_sre', 'enum', 'pydoc', 'xml', '_ssl', 'errno', 'pydoc_data', 'xmlrpc', '_stat', 'faulthandler', 'pyexpat', 'xpto', '_statistics', 'fcntl', 'queue', 'xxlimited', '_string', 'filecmp', 'quopri', 'xxlimited_35', '_strptime', 'fileinput', 'random', 'xxsubtype', '_struct', 'fnmatch', 're', 'zipapp', '_symtable', 'fractions', 'readline', 'zipfile', '_sysconfigdata__linux_x86_64-linux-gnu', 'ftplib', 'reprlib', 'zipimport', '_sysconfigdata__x86_64-linux-gnu', 'functools', 'resource', 'zlib', '_testbuffer', 'gc', 'rlcompleter', 'zoneinfo', '_testcapi', 'genericpath'])
    ```

### `#!py BUILTIN_FUNCTIONS`

Type: `#!py Final[Iterable[str]]`

Value: `#!py sorted(['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'])`

??? example "SNIPPET"

    ```py
    BUILTIN_FUNCTIONS: Final[Iterable[str]] = sorted(['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'])
    ```

### `#!py BUILTIN_DUNDER_METHODS`

Type: `#!py Final[Iterable[str]]`

Value: `#!py sorted(['__init__', '__new__', '__del__', '__repr__', '__str__', '__bytes__', '__format__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__hash__', '__bool__', '__getattr__', '__getattribute__', '__setattr__', '__delattr__', '__dir__', '__get__', '__set__', '__delete__', '__init_subclass__', '__set_name__', '__instancecheck__', '__subclasscheck__', '__class_getitem__', '__call__', '__len__', '__length_hint__', '__getitem__', '__setitem__', '__delitem__', '__missing__', '__iter__', '__reversed__', '__contains__', '__add__', '__radd__', '__iadd__', '__sub__', '__mul__', '__matmul__', '__truediv__', '__floordiv__', '__mod__', '__divmod__', '__pow__', '__lshift__', '__rshift__', '__and__', '__xor__', '__or__', '__neg__', '__pos__', '__abs__', '__invert__', '__complex__', '__int__', '__float__', '__index__', '__round__', '__trunc__', '__floor__', '__ceil__', '__enter__', '__exit__', '__await__', '__aiter__', '__anext__', '__aenter__', '__aexit__'])`

??? example "SNIPPET"

    ```py
    BUILTIN_DUNDER_METHODS: Final[Iterable[str]] = sorted(['__init__', '__new__', '__del__', '__repr__', '__str__', '__bytes__', '__format__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__hash__', '__bool__', '__getattr__', '__getattribute__', '__setattr__', '__delattr__', '__dir__', '__get__', '__set__', '__delete__', '__init_subclass__', '__set_name__', '__instancecheck__', '__subclasscheck__', '__class_getitem__', '__call__', '__len__', '__length_hint__', '__getitem__', '__setitem__', '__delitem__', '__missing__', '__iter__', '__reversed__', '__contains__', '__add__', '__radd__', '__iadd__', '__sub__', '__mul__', '__matmul__', '__truediv__', '__floordiv__', '__mod__', '__divmod__', '__pow__', '__lshift__', '__rshift__', '__and__', '__xor__', '__or__', '__neg__', '__pos__', '__abs__', '__invert__', '__complex__', '__int__', '__float__', '__index__', '__round__', '__trunc__', '__floor__', '__ceil__', '__enter__', '__exit__', '__await__', '__aiter__', '__anext__', '__aenter__', '__aexit__'])
    ```

### `#!py ACCEPTABLE_LOWER_CONSTANTS`

Type: `#!py Final[list[str]]`

Value: `#!py ['app', 'application', 'urlpatterns', 'app_name', 'main']`

??? example "SNIPPET"

    ```py
    ACCEPTABLE_LOWER_CONSTANTS: Final[list[str]] = ['app', 'application', 'urlpatterns', 'app_name', 'main']
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

Value: `#!py '\n# File: `{filename}`\nPath: `{filepath}`\n\n{filedoc}\n\n---\n\n## Imports\n\n{imports}\n\n---\n\n## Consts\n\n{constants}\n\n---\n\n## Classes\n\n{classes}\n\n---\n\n## Functions\n\n{functions}\n\n---\n\n## Assertions\n\n{assertions}\n'`

??? example "SNIPPET"

    ```py
    FILE_MARKDOWN: Final[str] = '\n# File: `{filename}`\nPath: `{filepath}`\n\n{filedoc}\n\n---\n\n## Imports\n\n{imports}\n\n---\n\n## Consts\n\n{constants}\n\n---\n\n## Classes\n\n{classes}\n\n---\n\n## Functions\n\n{functions}\n\n---\n\n## Assertions\n\n{assertions}\n'
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

Value: `#!py '### `#!py class {name}`\n\nParents: `{inherit}`\n\nDecorators: `#!py {decorators}`\n\nKwargs: `#!py {kwargs}` \n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n' `

??? example "SNIPPET"

    ```py
    CLASS_DEF_MD_STRUCT: Final[str] = '### `#!py class {name}`\n\nParents: `{inherit}`\n\nDecorators: `#!py {decorators}`\n\nKwargs: `#!py {kwargs}`\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n'
    ```

### `#!py FUNCTION_DEF_MD_STRUCT`

Type: `#!py Final[str]`

Value: `#!py '### `#!py def {name}`\n\nType: `#!py {category}`\n\nReturn Type: `#!py {rtype}`\n\nDecorators: `#!py {decorators}`\n\nArgs: `#!py {args}`\n\nKwargs: `#!py {kwargs}` \n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n' `

??? example "SNIPPET"

    ```py
    FUNCTION_DEF_MD_STRUCT: Final[str] = '### `#!py def {name}`\n\nType: `#!py {category}`\n\nReturn Type: `#!py {rtype}`\n\nDecorators: `#!py {decorators}`\n\nArgs: `#!py {args}`\n\nKwargs: `#!py {kwargs}`\n\n??? example "SNIPPET"\n\n    ```py\n{code}\n    ```\n\n'
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
