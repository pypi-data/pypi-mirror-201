# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['regexp_learner', 'regexp_learner.gold', 'regexp_learner.lstar']

package_data = \
{'': ['*']}

install_requires = \
['ipython', 'numpy>=1.24.2', 'pybgl>=0.9.3']

setup_kwargs = {
    'name': 'regexp-learner',
    'version': '0.2.1',
    'description': 'Python3 module providing some algorithms to infer automata and regular expressions."',
    'long_description': '# regexp-learner\n\n[![PyPI](https://img.shields.io/pypi/v/regexp_learner.svg)](https://pypi.python.org/pypi/regexp_learner/)\n[![Build](https://github.com/nokia/regexp-learner/workflows/build/badge.svg)](https://github.com/nokia/regexp-learner/actions/workflows/build.yml)\n[![Documentation](https://github.com/nokia/regexp-learner/workflows/docs/badge.svg)](https://github.com/nokia/regexp-learner/actions/workflows/docs.yml)\n[![ReadTheDocs](https://readthedocs.org/projects/regexp-learner/badge/?version=latest)](https://regexp-learner.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/nokia/regexp-learner/branch/master/graph/badge.svg?token=OZM4J0Y2VL)](https://codecov.io/gh/nokia/regexp-learner)\n\n## Overview\n\n[regexp-learner](https://github.com/nokia/regexp-learner) is a [Python 3](http://python.org/) module providing the following algorithms:\n* __Angluin (1987):__ the L* algorithm is presented in _Learning regular sets from queries and couterexamples_, Dana Angluin, 1987 [[pdf](https://people.eecs.berkeley.edu/~dawnsong/teaching/s10/papers/angluin87.pdf)].\n* __Gold (1978):__ the Gold algorithm is presented in _Complexity of automaton identification from given data_, E. Mark Gold, 1987 [[pdf](http://sebastian.doc.gold.ac.uk/papers/Language_Learning/gold78complexity.pdf)].\n\nThis module is built on top of:\n* [numpy](https://pypi.org/project/numpy/);\n* [pybgl](https://pypi.org/project/pybgl/), a lightweight graph library.\n\nA [jupyter notebook](https://pypi.org/project/jupyter/) is also provided test the algorithm. Note that the [graphviz](https://pypi.org/project/jupyter/) runnables (e.g., `dot`) is required to display the automata.\n\n## Usage\n\n* Install [Jupyter Notebook](https://pypi.org/project/jupyter/) or [Jupyter lab](https://pypi.org/project/jupyterlab/).\n* Follow [installation steps](https://github.com/nokia/regexp-learner/wiki/Installation).\n* Run `jupyter notebook` or `jupyter lab`.\n* Open the desired notebook.\n* Run the cells.\n\n\n## Links\n\n* [Installation](https://github.com/nokia/regexp-learner/wiki/Installation)\n* [Tests](https://github.com/nokia/regexp-leader/wiki/Test)\n\n## License\n\nThis project is licensed under the [BSD-3-Clause license](https://github.com/nokia/regexp-learner/blob/master/LICENSE).\n',
    'author': 'Marc-Olivier Buob',
    'author_email': 'marc-olivier.buob@nokia-bell-labs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
