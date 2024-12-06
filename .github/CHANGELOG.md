# Changelog and Update History

A changelog is a document that tracks the history of changes in a project, typically organized by version numbers. It serves as a transparent record for developers, users, and contributors, detailing what has been added, updated, fixed, removed, or addressed in terms of security. By offering a structured overview, changelogs play a vital role in maintaining trust, facilitating communication, and easing version management.

Changelogs provide a transparent narrative of a project’s evolution. They ensure users can make informed decisions about updating software and give contributors insights into the project’s direction. For development teams, changelogs are invaluable for version control and accountability. Well-maintained changelogs foster trust, improve user engagement, and ensure smoother project management for all stakeholders.

Key Components of a Changelog:

- Adds: This section highlights new features, tools, or functionalities introduced to the project. For example, a CLI tool may include a new command or configuration option. Clearly listing these additions allows users to discover improvements and expanded capabilities.
- Updates: Updates reflect modifications or enhancements to existing features, such as performance optimizations or UI/UX improvements. These entries help users understand what has evolved, ensuring they benefit from improved usability or efficiency.
- Fixes: Fixes document the resolution of bugs or issues. By specifying what was corrected, users gain confidence that problems they may have encountered have been addressed, reducing frustration.
- Removes: Sometimes, features or functionalities are deprecated or removed. Listing these changes prevents surprises, enabling users to adapt and refactor their workflows accordingly.
- Security: Security changes focus on vulnerabilities that have been mitigated or resolved. This section reassures users that the project maintains high standards for safety and data protection.

---

<!--

## {VERSION} - {DATE}

### Adds

- Item

### Updates

- Item

### Fixes

- Item

### Removes

- Item

### Security

- Item

-->

## v1.1.0 - 2024-12-06

### Adds

- Creation of `CHANGELOG.md`
- `setup.py` into `README.md` dir's demonstration
- `documentation` into `README.md` dir's demonstration
- `--edit-uri` parameter defined as `'blob/main/documentation/docs'`

### Updates

- `README.md`'s todo list targets
- `--exit` parameter renamed to `--output`
- `--logo-path` argument's defaults to `None`
- `--readme-path` argument's defaults to `None`
- `clickable_checkbox` statement of `mkdocs.yml` defaults to `false`
- Some function docstrings reviewed

## v1.0.0 - 2024-12-04

### Adds

- First stable version release
