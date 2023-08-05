# sc_inetbox_adapter

API adapter for Swisscom Internet Box

## Installation

```bash
$ pip install sc_inetbox_adapter
```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`sc_inetbox_adapter` was created by Matthias Weis. It is licensed under the terms of the GNU General Public License v3.0 license.

## Develop

In the root dir:
```bash
$ python -m venv .
$ source ./bin/activate
$ poetry install
```

## Test
Place a file named '''.password''' containing the admin password in the root folder and run the tests:
```bash
$ python -m pytest tests
```

## Publish
```bash
poetry config pypi-token.test-pypi *TOKEN*
poetry publish -r test-pypi
```

## Credits

`sc_inetbox_adapter` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
