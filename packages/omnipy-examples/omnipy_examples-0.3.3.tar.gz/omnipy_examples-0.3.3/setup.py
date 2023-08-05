# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['omnipy_examples']

package_data = \
{'': ['*']}

install_requires = \
['github3-py>=3.2.0,<4.0.0',
 'omnipy-example-data>=0.1.0,<0.2.0',
 'omnipy>=0.10.3,<0.11.0',
 'reader>=3.4,<4.0',
 's3fs>=2023.1.0,<2024.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'typing-inspect>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['omnipy-examples = omnipy_examples.main:app']}

setup_kwargs = {
    'name': 'omnipy-examples',
    'version': '0.3.3',
    'description': '',
    'long_description': '# omnipy-examples\n\nExample projects that that makes use of the [omnipy](https://pypi.org/project/omnipy/) package for \ntype-driven, scalable and interoperable data wrangling!\n\n## Main installation instructions\n\n- Install:\n  - `pip install omnipy-examples`\n- Run example scripts:\n  - Example: `omnipy-examples isajson`\n  - For help on the command line interface: `omnipy-examples --help`\n  - For help on a particular example: `omnipy-examples isajson --help`\n\n### Output of flow runs\n\nThe output will by default appear in the `data` directory, with a timestamp. \n\n  - It is recommended to install a file viewer that are capable of browsing tar.gz files. \n    For instance, the "File Expander" plugin in PyCharm is excellent for this.\n  - To unpack the compressed files of a run on the command line \n    (just make sure to replace the datetime string from this example): \n\n```\nfor f in $(ls data/2023_02_03-12_51_51/*.tar.gz); do mkdir ${f%.tar.gz}; tar xfzv $f -C ${f%.tar.gz}; done\n```\n    \n### Run with the Prefect engine\n\nOmnipy is integrated with the powerful [Prefect](https://prefect.io) data flow orchestration library.\n\n- To run an example using the `prefect` engine, e.g.:\n  - `omnipy-examples --engine prefect isajson`\n- After completion of some runs, you can check the flow logs and orchestration options in the Prefect UI:\n  - `prefect orion start`\n\nMore info on Prefect configuration will come soon...\n\n## Development setup\n\n- Install Poetry:\n  - `curl -sSL https://install.python-poetry.org | python3 -`\n\n- Install dependencies:\n  - `poetry install --with dev`\n\n### For mypy support in PyCharm\n\n- In PyCharm, install "Mypy" plugin (not "Mypy (Official)")\n  - `which mypy` to get path to mypy binary\n  - In the PyCharm settings for the mypy plugin:\n    - Select the mypy binary \n    - Select `pyproject.toml` as the mypy config file\n\n### For automatic formatting and linting\n\nI have added my typical setup for automatic formatting and linting. The main alternative is to use black, which is easier to set up, but it does \nnot have as many options. I am not fully happy with my config, but I at least like it better than black. \n\n- In PyCharm -> File Watchers:\n  - Click arrow down icon\n  - Select `watchers.xml`\n',
    'author': 'Sveinung Gundersen',
    'author_email': 'sveinugu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
