# PyPBar

[![Hits-of-Code](https://hitsofcode.com/github/koviubi56/pypbar?branch=main)](https://hitsofcode.com/github/koviubi56/pypbar/view?branch=main)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7b37a885e4454ac0aeba1721197712a9)](https://www.codacy.com/gh/koviubi56/pypbar/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=koviubi56/pypbar&amp;utm_campaign=Badge_Grade)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/koviubi56/pypbar)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/koviubi56/pypbar/main.svg)](https://results.pre-commit.ci/latest/github/koviubi56/pypbar/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![semantic-release](https://img.shields.io/badge/%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)
![GitHub](https://img.shields.io/github/license/koviubi56/pypbar)
![PyPI](https://img.shields.io/pypi/v/pypbar)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypbar)
![PyPI - Format](https://img.shields.io/pypi/format/pypbar)

PyPBar is a [Python library](https://docs.python.org/3/glossary.html#term-module) for dealing with [progress bars](https://en.wikipedia.org/wiki/Progress_bar).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyPBar. _[Need more help?](https://packaging.python.org/en/latest/tutorials/installing-packages/)_

```bash
pip install pypbar
```

## Requirements

PyPBar requires Python 3.7 and `typing_extensions>=4.0.0`. _[See the `requirements.txt`](requirements.txt)_

## Usage

```py
import pypbar
import time

with pypbar.Bar(10) as bar:
    for n in bar:
        time.sleep(1)

with pypbar.Bar(["the", "quick", "brown", "fox"]) as bar:
    for w in bar:
        # Instead of print() you should use .write()
        bar.write(w)
        time.sleep(2)
```

## Support

Questions should be asked in the [Discussions tab](https://github.com/koviubi56/pypbar/discussions/categories/q-a).

Feature requests and bug reports should be reported in the [Issues tab](https://github.com/koviubi56/pypbar/issues/new/choose).

Security vulnerabilities should be reported as described in our [Security policy](https://github.com/koviubi56/pypbar/security/policy) (the [SECURITY.md](SECURITY.md) file).

## Contributing

[Pull requests](https://github.com/koviubi56/pypbar/blob/main/CONTRIBUTING.md#pull-requests) are welcome. For major changes, please [open an issue first](https://github.com/koviubi56/pypbar/issues/new/choose) to discuss what you would like to change.

Please make sure to add entries to [the changelog](CHANGELOG.md).

For more information, please read the [contributing guidelines](CONTRIBUTING.md).

## Authors and acknowledgments

A list of nice people who helped this project can be found in the [CONTRIBUTORS file](CONTRIBUTORS).

## License

[GNU GPLv3+](LICENSE)
