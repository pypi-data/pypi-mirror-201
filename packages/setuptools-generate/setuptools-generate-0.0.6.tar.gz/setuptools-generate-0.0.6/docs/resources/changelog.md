# Generate Changelog

Sometimes, you have a changelog like this: (See
[frinyvonnick/gitmoji-changelog](https://github.com/frinyvonnick/gitmoji-changelog))

````markdown
```{eval-sh}
cd ..
cat tests/changelog/CHANGELOG.md
```
````

This tool can generate a `build/CHANGELOG.md`.

````html
```{eval-sh}
cd ..
cat tests/changelog/test/CHANGELOG.md
```
````

So you can

```yaml
  - uses: softprops/action-gh-release@v1
    if: startsWith(github.ref, 'refs/tags/')
    with:
      body_path: build/CHANGELOG.md
      files: |
        dist
        sdist
```

More information can be seen in
[softprops/action-gh-release](https://github.com/softprops/action-gh-release).
