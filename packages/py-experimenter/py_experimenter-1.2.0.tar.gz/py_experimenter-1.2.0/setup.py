# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_experimenter']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0',
 'jupyterlab>=3.5.0,<4.0.0',
 'mysql-connector-python>=8.0',
 'numpy>=1.15',
 'pandas>=1.0']

setup_kwargs = {
    'name': 'py-experimenter',
    'version': '1.2.0',
    'description': 'The PyExperimenter is a tool for the automatic execution of experiments, e.g. for machine learning (ML), capturing corresponding results in a unified manner in a database.',
    'long_description': '[![doc](https://img.shields.io/badge/doc-success-success)](https://tornede.github.io/py_experimenter)\n[![pypi](https://img.shields.io/pypi/v/py_experimenter)](https://pypi.org/project/py-experimenter/)\n[![GitHub](https://img.shields.io/github/license/tornede/py_experimenter)](https://tornede.github.io/py_experimenter/license.html)\n\n<img src="docs/source/_static/py-experimenter-logo.png" alt="PyExperimenter Logo: Python biting a database" width="200px"/>\n\n# PyExperimenter\n\n`PyExperimenter` is a tool to facilitate the setup, documentation, execution, and subsequent evaluation of results from an empirical study of algorithms and in particular is designed to reduce the involved manual effort significantly.\nIt is intended to be used by researchers in the field of artificial intelligence, but is not limited to those.\n\nThe empirical analysis of algorithms is often accompanied by the execution of algorithms for different inputs and variants of the algorithms (specified via parameters) and the measurement of non-functional properties.\nSince the individual evaluations are usually independent, the evaluation can be performed in a distributed manner on an HPC system.\nHowever, setting up, documenting, and evaluating the results of such a study is often file-based.\nUsually, this requires extensive manual work to create configuration files for the inputs or to read and aggregate measured results from a report file.\nIn addition, monitoring and restarting individual executions is tedious and time-consuming.\n\nThese challenges are addressed by `PyExperimenter` by means of a single well defined configuration file and a central database for managing massively parallel evaluations, as well as collecting and aggregating their results.\nThereby, `PyExperimenter` alleviates the aforementioned overhead and allows experiment executions to be defined and monitored with ease.\n\n![General schema of `PyExperimenter`.](docs/source/_static/workflow.png)\n\nFor more details check out the [`PyExperimenter` documentation](https://tornede.github.io/py_experimenter/):\n\n- [Installation](https://tornede.github.io/py_experimenter/installation.html)\n- [Examples](https://tornede.github.io/py_experimenter/examples/example_general_usage.html)\n',
    'author': 'Tanja Tornede',
    'author_email': 't.tornede@ai.uni-hannover.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tornede/py_experimenter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
