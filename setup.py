from setuptools import find_packages, setup

from mosheh.main import __version__ as mosheh_version


with open('.github/README.md', encoding='utf-8') as f:
    content: str = f.read()

setup(
    name='mosheh',
    version=mosheh_version,
    packages=find_packages(),
    install_requires=[
        'mkdocs==1.6.1',
        'mkdocs-material==9.5.47',
        'mkdocs-material-extensions==1.3.1',
        'mkdocs-git-revision-date-localized-plugin==1.3.0',
    ],
    entry_points={
        'console_scripts': [
            'mosheh=mosheh.main:main',
        ],
    },
    author='Lucas Gonçalves da Silva',
    author_email='lucasgoncsilva04@gmail.com',
    description='Mosheh, a tool for creating docs for projects, from Python to Python.',
    long_description=content,
    long_description_content_type='text/markdown',
    url='https://github.com/LucasGoncSilva/mosheh',
    license='MIT',
    keywords=[
        'CLI',
        'Python',
        'documentation',
        'MkDocs',
        'automation',
        'generation',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Code Generators',
        'Topic :: System :: Filesystems',
        'Topic :: Text Processing :: Markup :: Markdown',
        'Development Status :: 5 - Production/Stable',
    ],
)
