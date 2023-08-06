# The Intention of This Tool

## Dependencies

There are many different types of dependencies: (The following syntax is
`pyproject.toml`, you can write `requirements.txt` freely if you prefer it.)

### Build dependencies

Needed when packagers and CI/CD are building a python project.

```toml
[build-system]
dependencies = [ "XXX", "YYY",]
```

### Runtime dependencies

Needed when users run a python program. If they are not installed, the program
will fail.

```toml
[project]
dependencies = [ "XXX", "YYY",]
```

### Extra dependencies

Needed when users run a python program to realize some extra functions. If they
are not installed, the program will lose some function.

```toml
[project.optional-dependencies]
function_name = [ "XXX", "YYY",]
```

### Develop dependencies

A special extra dependency which just for developers and CI/CD run some test like

- unit test
- code coverage
- pre commit hooks for linters, formatters, grammar checkers, spell checkers, ...

```toml
[project.optional-dependencies]
dev = [ "XXX", "YYY",]
```

### Document build dependencies

Only for document build.

```toml
[project.optional-dependencies]
docs = [ "XXX", "YYY",]
```

### Conclusion

1. Developers write code and tests, then let CI/CD test (install develop
   dependencies), build (if test pass, install build dependencies) and release
   (if build pass).
2. Packagers download the released packages (for python, it is a wheel file)
   and repackage them to packages of debian, rpm, pacman, portage, homebrew,
   nix, etc.
3. Users use their package managers to download the package and install them to
   their software distributions like Windows msys2, Android termux, Android
   termux-pacman, Linux and macOS's homebrew, Linux and macOS's nix, etc
   (install runtime dependencies and some extra dependencies).

## The Aim of This Tool

Any software is not only consisted of executable files and necessary libraries,
it also contains some resources like shell completions, man pages, desktop
entries, icons, etc. Some resources, like shell completions and man pages, can
be generated from executable files. So who should generate them? Developers or
packagers?

Obviously, developers build once, all packagers of different package managers
can use the built resources without repeatedly building them. For developers,
it just write some code to let CI/CD do this job.

Usually, developers build these resources in the test job of CI/CD and install
some packages needed by building these resource as develop dependencies.
However, these packages are not truly related to any test. It increases the
redundant dependencies in test job, which is not pure (Although we don't need
a absolute pure environment like nix or docker, pure is better than impure).
And the other dependencies for test job is also possible to effect these
resources' building.

Or developers create a new job named build-resource in CI/CD. Although it
increases some troubles, it is also acceptable.

Why not let them become build
dependencies? If so, we can use CI/CD to build all resources needed for
release, then just release them together:

```yaml
# ...
jobs:
  # ...
  build:
    # ...
    steps:
      # ...
      - name: Build
        run: |
          pip install build
          python -m build
      - uses: actions/upload-artifact@v3
        if: ${{ ! startsWith(github.ref, 'refs/tags/') }}
        with:
          path: |
            dist/*
            sdist/*
      - uses: softprops/action-gh-release@v1
        if: startsWith(github.ref, 'refs/tags/')
        with:
          files: |
            dist/*
            sdist/*
      - uses: pypa/gh-action-pypi-publish@release/v1
        if: startsWith(github.ref, 'refs/tags/') && runner.os == 'Linux'
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

## Pits

However, a trouble is: we need to run the executable file to build some
resources in build job. It imports runtime dependencies to build
dependencies. In order to reduce the imported dependencies, the entry of
program should be designed carefully.

```python
#!/usr/bin/env python
"""A template for ``__main__.py``."""
from argparse import ArgumentParser
from contextlib import suppress

# Users don't need to install build dependencies
with suppress(ImportError):
    import shtab


def get_parser() -> ArgumentParser:
    """Get parser for ``main()`` and unit test."""
    parser = ArgumentParser()
    with suppress(NameError):
        shtab.add_argument_to(parser)
    # ...
    return parser


def main() -> None:
    """This module can be called by
    `python -m <https://docs.python.org/3/library/__main__.html>`_.

    Wrap the mostly logic to ``run()``, because ``--help``, ``--version``,
    ``--print-completion`` will exit on ``parser.parse_args()``. The following
    code of ``run()`` will not be sourced. It will save time for those users
    who just want to see the usage of this program by ``--help`` without
    sourcing ``run()``, especially when ``run()`` import many large libraries,
    it will be very slow.
    """
    parser = get_parser()
    args = parser.parse_args()
    if args.gui:
        from .ui.gui import run
    else:
        from .ui.cli import run
    run()


if __name__ == "__main__":
    main()
```

Now all runtime dependencies are imported in `run()`, where not be imported on
building shell completions.

`__init__.py` is likely.

## Support

Currently, this tool support:

- [shtab](https://pypi.org/project/shtab) provides bash/zsh/tcsh completions.
  It can be removed from runtime dependencies.
- [click](https://pypi.org/project/click) provides bash/zsh/fish completions.
  It also parses command line arguments, so it cannot be removed from runtime
  dependencies.
- [help2man](https://pypi.org/project/help2man) provides man pages. Just build
  dependencies.

## Install

It is unnecessary to install this tool directly because it is just a
setuptools plugin and have no other usages. Its aim is to become a build
dependency of a python project which need to build some resources.
