from custom_types import Lang


def generate_doc(
    exit: str,
    proj_name: str,
    lang: Lang,
    edit_uri: str = '',
    repo_name: str = 'GitHub',
    repo_url: str = '',
) -> None:
    base_yml: str = default_doc_config(
        proj_name,
        edit_uri,
        lang,
        repo_name,
        repo_url,
    )


def default_doc_config(
    proj_name: str,
    edit_uri: str,
    lang: Lang,
    repo_name: str = 'GitHub',
    repo_url: str = '',
) -> str:
    return f"""site_name: {proj_name} | Documentation
repo_url: {repo_url}
repo_name: {repo_name}
edit_uri: "{edit_uri}"


theme:
  name: material
  language: {lang}
  # TODO: favicon: fontawesome/solid/book-open
  font:
    text: Ubuntu
  custom_dir: overrides

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
      RID: fontawesome/solid/building
      OE: fontawesome/solid/gavel
  
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
      primary: custom
      accent: deep purple

    # Palette toggle for light mode
    - scheme: default
      toggle:
        icon: material/brightness-7
        name: Light/Dark Mode
      primary: custom
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
    RID: RID
    OE: OE

  status:
    new: Adicionado recentemente

  social:
    - icon: material/microsoft-azure
      link: https://dev.azure.com/ONR-RID/PROJETO_ONR.TESTESAUTOMACAO
      name: Projeto Azure

    - icon: material/instagram
      link: https://www.instagram.com/registrodeimoveis.onr/
      name: Instagram ONR

    - icon: material/facebook
      link: https://facebook.com/registrodeimoveis.onr/
      name: Facebook ONR

    - icon: material/linkedin
      link: https://br.linkedin.com/company/operador-nacional-do-registro-eletr%C3%B4nico-de-im%C3%B3veis-onr
      name: LinkedIn ONR

    - icon: material/youtube
      link: https://www.youtube.com/@registrodeimoveiseletronico/videos
      name: YouTube ONR


extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js


extra_css:
  - stylesheets/extra.css


copyright: No copyright 'cause no one supports me :("""
