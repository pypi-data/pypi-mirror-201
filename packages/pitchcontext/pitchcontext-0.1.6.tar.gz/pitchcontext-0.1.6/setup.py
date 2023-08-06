# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pitchcontext']

package_data = \
{'': ['*']}

install_requires = \
['IPython>=7.19,<8.0',
 'matplotlib>=3.3,<4.0',
 'music21>=8.0,<9.0',
 'numpy>=1.19,<2.0',
 'seaborn>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'pitchcontext',
    'version': '0.1.6',
    'description': 'Library for melody analysis based on pitch context vectors.',
    'long_description': '---\ncomponent-id: pitchcontext\nname: pitchcontext\ndescription: Python module for melody analysis based on pitch context vectors.\ntype: Library\nrelease-date: 2023-03-15\nrelease-number: 0.1.4\nwork-package: WP3\npilot: TUNES\nkeywords:\n  - melody\n  - pitch analysis\nchangelog:\nlicence:\nrelease link:\n--- \n\n\n# pitchcontext\nPython module for melody analysis based on pitch context vectors.\n\n## Prerequisites:\n- lilypond installed and in command line path\n- convert (ImageMagick) installed and in command line path\n- kernfiles and corresponding .json files with melodic features\n\n## Installation\nThe latest release of the pitchcontext module can be installed from pypi:\n```\n$ pip install pitchcontext\n```\n\nThe development version can be installed by cloning the repository and by using the provided pyproject.toml and poetry. In root of the rep do:\n```\n$ poetry install\n```\nThis creates a virtual environment with pitchcontext installed.\n\n## Examples\nRequires a Python3 environment with both pitchcontext and streamlit installed.\nTwo examples are provided:\n- apps/st_dissonance.py\n- apps/st_novelty.py\n\nTo run:\n```\n$ streamlit run st_dissonance.py -- -krnpath <path_to_kern_files> -jsonpath <path_to_json_files>\n```\n',
    'author': 'Peter van Kranenburg',
    'author_email': 'peter.van.kranenburg@meertens.knaw.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
