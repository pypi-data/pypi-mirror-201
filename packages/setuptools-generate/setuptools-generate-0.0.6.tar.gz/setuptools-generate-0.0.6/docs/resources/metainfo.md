# Generate Metainfo

This tool also support generating some metainfo to a file like

````python
```{eval-sh}
cd ..
cat src/setuptools_generate/_metainfo.py
```
````

Just

```toml
[tool.setuptools-generate]
write-to = "src/translate_shell/_metainfo.py"
```

You can customize template by

```toml
[tool.setuptools-generate]
write-to = "src/translate_shell/_metainfo.py"

[tool.setuptools-generate.metainfo-template]
text = "XXXXX"
```

or

```toml
[tool.setuptools-generate]
write-to = "src/translate_shell/_metainfo.py"

[tool.setuptools-generate.metainfo-template]
file = "XXXXX"
```

The template language is
[jinja2](https://docs.jinkan.org/docs/jinja2/templates.html):

````jinja
```{eval-sh}
cd ..
cat src/setuptools_generate/assets/jinja2/metainfo.py.j2
```
````

## sphinx

For sphinx's `docs/conf.py`, just

```python
from translate_shell._metainfo import author, copyright, project
```

You don't need write these metainfo twice: in `pyproject.toml` and
`docs/conf.py`.

## help2man

For help2man, just in your `__main__.py`:

```python
from argparse import ArgumentParser
from translate_shell._metainfo import author, copyright, project


def get_parser():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EPILOG)
    parser.add_argument("--version", action="version", version=VERSION)
```
