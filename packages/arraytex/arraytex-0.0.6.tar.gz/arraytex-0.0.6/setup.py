# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arraytex']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'numpy>=1.24.2,<2.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'typing-extensions>=4.5.0,<5.0.0']

entry_points = \
{'console_scripts': ['arraytex = arraytex.__main__:main']}

setup_kwargs = {
    'name': 'arraytex',
    'version': '0.0.6',
    'description': 'ArrayTeX',
    'long_description': "# ArrayTeX\n\n[![PyPI](https://img.shields.io/pypi/v/arraytex.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/arraytex.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/arraytex)][python version]\n[![License](https://img.shields.io/pypi/l/arraytex)][license]\n\n[![Read the documentation at https://arraytex.readthedocs.io/](https://img.shields.io/readthedocs/arraytex/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/dbatten5/arraytex/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/dbatten5/arraytex/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/arraytex/\n[status]: https://pypi.org/project/arraytex/\n[python version]: https://pypi.org/project/arraytex\n[read the docs]: https://arraytex.readthedocs.io/\n[tests]: https://github.com/dbatten5/arraytex/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/dbatten5/arraytex\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nConvert a `numpy.NDArray` to various LaTeX forms.\n\n```python\n>>> import numpy as np\n>>> import arraytex as atx\n>>> A = np.array([[1, 2, 3], [4, 5, 6]])\n>>> print(atx.to_matrix(A))\n\\begin{bmatrix}\n1 & 2 & 3 \\\\\n4 & 5 & 6 \\\\\n\\end{bmatrix}\n```\n\nInspired by [@josephcslater](https://github.com/josephcslater)'s\n[array_to_latex](https://github.com/josephcslater/array_to_latex).\n\n## Features\n\n- Support for different matrix environment delimiters (`bmatrix` or `pmatrix`).\n- Support for tabular environments.\n- Support for builtin number formats (`:.2f`, `:.3e`, etc.).\n- Fully tested and typed.\n\n## Requirements\n\n- `python >= 3.8`\n\n## Installation\n\nYou can install _ArrayTeX_ via [pip] from [PyPI]:\n\n```console\n$ pip install arraytex\n```\n\n## Usage\n\nPlease see the [docs](https://arraytex.readthedocs.io/) for more information.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_ArrayTeX_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/dbatten5/arraytex/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/dbatten5/arraytex/blob/main/LICENSE\n[contributor guide]: https://github.com/dbatten5/arraytex/blob/main/CONTRIBUTING.md\n[command-line reference]: https://arraytex.readthedocs.io/en/latest/usage.html\n",
    'author': 'Dom Batten',
    'author_email': 'dominic.batten@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dbatten5/arraytex',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
