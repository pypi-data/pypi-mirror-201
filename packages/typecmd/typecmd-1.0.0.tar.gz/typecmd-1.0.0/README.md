This is a command tootset used in my work.

## System requirements

[install poetry](https://python-poetry.org/docs/#installation)

## How to install

```sh
pipx install typecmd
```

## How to use

After installed, you can use command directory in this toolset.

For example:

```
yaml2json --help
```

## How to build

clone source

```sh
git clone https://github.com/telesoho/typecmd.git
```

```sh
cd typecmd
poetry install
poetry build
```

Active shell

```sh
poetry shell
```

use pipx to install the cli commands.

```sh
pipx install dist/typecmd-<version>.tar.gz
```

Now you can use `typecmd`.

```sh
typecmd --help
```
