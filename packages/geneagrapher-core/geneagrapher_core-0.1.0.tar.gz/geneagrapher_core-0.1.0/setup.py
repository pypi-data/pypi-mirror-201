# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geneagrapher_core']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'types-beautifulsoup4>=4.11.6.4,<5.0.0.0']

setup_kwargs = {
    'name': 'geneagrapher-core',
    'version': '0.1.0',
    'description': 'Functions for getting records and building graphs from the Math Genealogy Project.',
    'long_description': "# geneagrapher-core [![Continuous Integration Status](https://github.com/davidalber/geneagrapher-core/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/davidalber/geneagrapher-core/actions/workflows/ci.yaml/badge.svg?branch=main) [![Live Tests Status](https://github.com/davidalber/geneagrapher-core/actions/workflows/live-tests.yaml/badge.svg?branch=main)](https://github.com/davidalber/geneagrapher-core/actions/workflows/live-tests.yaml/badge.svg?branch=main) [![Documentation Status](https://readthedocs.org/projects/geneagrapher-core/badge/?version=latest)](https://geneagrapher-core.readthedocs.io/en/latest/?badge=latest)\n\n## Overview\nGeneagrapher is a tool for extracting information from the\n[Mathematics Genealogy Project](https://www.mathgenealogy.org/) to\nform a math family tree, where connections are between advisors and\ntheir students.\n\nThis package contains the core data-grabbing and manipulation\nfunctions needed to build a math family tree. The functionality here\nis low level and intended to support the development of other\ntools. If you just want to build a geneagraph, take a look at\n[Geneagrapher](https://github.com/davidalber/geneagrapher). If you\nwant to get mathematician records and use them in code, then this\nproject may be useful to you.\n\n## Documentation\nDocumentation about how to call into this package's functions can be\nfound at http://geneagrapher-core.readthedocs.io/.\n\n## Development\nDependencies in this package are managed by\n[Poetry](https://python-poetry.org/). Thus, your Python environment\nwill need Poetry installed. Install all dependencies with:\n\n```sh\n$ poetry install\n```\n\nSeveral development commands are runnable with `make`:\n- `make fmt` (also `make black` and `make format`) formats code using\n  black\n- `make format-check` runs black and reports if the code passes\n  formatting checks without making changes\n- `make lint` (also `make flake8` and `make flake`) does linting\n- `make mypy` (also `make types`) checks the code for typing violations\n- `make test` runs automated tests\n- `make check` does code formatting (checking, not modifying),\n  linting, type checking, and testing in one command; if this command\n  does not pass, CI will not pass\n",
    'author': 'David Alber',
    'author_email': 'alber.david@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davidalber/geneagrapher-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
