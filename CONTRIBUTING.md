<!--
Copyright (C) 2025 DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
-->

# Contributing to pmidcite

We welcome contributions to pmidcite,
whether it's through reporting bugs,
improving the documentation,
testing releases,
engaging in discussion on features and bugs,
or writing code.

## Table of Contents
 * [Code of Conduct](#code-of-conduct)
 * [Reporting Bugs](#reporting-bugs)
 * [Editing Documentation](#editing-documentation)
 * [Testing](#testing)
 * [Submitting feature requests and ideas](#submitting-feature-requests-and-ideas)
 * [Developing pmidcite](#developing)

## Code of Conduct

Before starting, please read the
[Code of Conduct](https://github.com/dvklopfenstein/pmidcite/blob/main/CODE_OF_CONDUCT.md).

## Reporting Bugs

Please report bugs by
[opening a new issue](https://github.com/dvklopfenstein/pmidcite/issues/new/choose)
and describing it as well as possible.
Many bugs are specific to a particular operating system and Python version, so please include that information!

## Editing Documentation

If you find a typo or a mistake in the docs,
please fix it right away and send a pull request.
If you're unsure what to change but still see a problem, you can
[open a new issue](https://github.com/dvklopfenstein/pmidcite/issues/new/choose)
with the "Documentation change" type.

To edit the documentation, edit the `docs/*.md` files on the **main** branch.
You can see the result by running `make mkdoc` inside the project's root directory,
then navigating your browser to [localhost:8000](http://localhost:8000).

### External editors and tips and tricks

If you'd like to share a pmidcite command line trick that you find useful,
you may find it worthwhile to add it to the
["Tips and Tricks" section](tips-and-tricks.md).

## Testing

Much of the work of maintaining pmidcite involves testing rather than coding.
We welcome tests.

## Submitting feature requests and ideas

If you have a feature request or idea for pmidcite, please
[open a new issue](https://github.com/dvklopfenstein/pmidcite/issues/new/choose)
and describe the goal of the feature, and any relevant use cases.
We'll discuss the issue with you, and decide if it's a good fit for the project.

When discussing new features, please keep in mind our design goals. pmidcite strives to
[do one thing well](https://en.wikipedia.org/wiki/Unix_philosophy). To us, that means:

* being _nimble_
* having a simple interface
* avoiding duplicating functionality

## Developing

Pull requests should be made on the `main` branch.

### Updating automated tests

When resolving bugs or adding new functionality,
please add tests to prevent that functionality from breaking in the future.
If you notice any functionality that isn't covered in the tests,
feel free to submit a test-only pull request as well.

For testing, pmidcite uses [pytest](https://docs.pytest.org) for unit tests.
All tests are in the `tests` folder.

### Submitting pull requests

When you're ready, feel free to submit a pull request (PR).
The continuous integration pipeline will
run automated tests on your PR and will report back any issues
it has found with your code across a variety of environments.

The pull request template contains a checklist full of housekeeping items. Please fill them out as necessary when you submit.

If a pull request contains failing tests,
it probably will not be reviewed,
and it definitely will not be approved.
However, if you need help resolving a failing test, please mention that in your PR.

### Finding things to work on

You can search the
[pmidcite GitHub issues](https://github.com/dvklopfenstein/pmidcite/issues) by
[label](https://github.com/dvklopfenstein/pmidcite/labels)
for things to work on. Here are some labels worth searching:

* [bug](https://github.com/dvklopfenstein/pmidcite/labels/bug)
* [documentation](https://github.com/dvklopfenstein/pmidcite/labels/documentation)
* [duplicate](https://github.com/dvklopfenstein/pmidcite/labels/duplicate)
* [enhancement](https://github.com/dvklopfenstein/pmidcite/labels/enhancement)
* [good first issue](https://github.com/dvklopfenstein/pmidcite/labels/good%20first%20issue)
* [help wanted](https://github.com/dvklopfenstein/pmidcite/labels/help%20wanted)
* [invalid](https://github.com/dvklopfenstein/pmidcite/labels/invalid)
* [question](https://github.com/dvklopfenstein/pmidcite/labels/question)
* [wontfix](https://github.com/dvklopfenstein/pmidcite/labels/wontfix)

### A note for new programmers and programmers new to Python

If you have a question, please don't hesitate to ask!
Python is known for its welcoming community and openness to novice programmers,
so feel free to fork the code and play around with it!
If you create something you want to share with us, please create a pull request.
We never expect pull requests to be perfect, idiomatic, instantly mergeable code.
We can work through it together!

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
