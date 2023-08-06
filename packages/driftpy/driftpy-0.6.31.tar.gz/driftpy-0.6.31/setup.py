# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['driftpy', 'driftpy.constants', 'driftpy.idl', 'driftpy.math', 'driftpy.setup']

package_data = \
{'': ['*']}

install_requires = \
['anchorpy==0.10.0',
 'mkdocs>=1.3.0,<2.0.0',
 'pythclient==0.1.2',
 'requests>=2.28.1,<3.0.0',
 'solana>=0.25.0,<0.26.0',
 'types-requests>=2.28.9,<3.0.0']

setup_kwargs = {
    'name': 'driftpy',
    'version': '0.6.31',
    'description': 'A Python client for the Drift DEX',
    'long_description': '# DriftPy\n\n<div align="center">\n    <img src="docs/img/drift.png" width="30%" height="30%">\n</div>\n\nDriftPy is the Python client for the [Drift](https://www.drift.trade/) protocol. It allows you to trade and fetch data from Drift using Python.\n\n**[Read the full SDK documentation here!](https://drift-labs.github.io/driftpy/)**\n\n## Installation\n\n```\npip install driftpy\n```\n\nNote: requires Python >= 3.10.\n\n## SDK Examples\n\n- `examples/` folder includes more examples of how to use the SDK including how to provide liquidity/become an lp, stake in the insurance fund, etc.\n\n## Setting Up Dev Env\n\n`bash setup.sh`\n\n## Running Unit Tests\n\n`bash test.sh`\n\n## Building the docs\n\nLocal Docs: `mkdocs serve` \n\nUpdating public docs: `poetry run mkdocs gh-deploy --force`\n\n## Releasing a new version of the package\n\n- `python new_release.py`\n- Create a new release at https://github.com/drift-labs/driftpy/releases.\n  - (The CI process will upload a new version of the package to PyPI.)',
    'author': 'x19',
    'author_email': 'https://twitter.com/0xNineteen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drift-labs/driftpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
