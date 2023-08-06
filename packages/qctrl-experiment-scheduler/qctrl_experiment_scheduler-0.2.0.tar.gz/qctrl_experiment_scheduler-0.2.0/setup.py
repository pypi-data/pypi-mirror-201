# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlexperimentscheduler', 'qctrlexperimentscheduler.predefined']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.7,<3.0',
 'numpy>=1.23.5,<2.0.0',
 'qctrl-commons>=18.0.0,<19.0.0',
 'qctrl-visualizer>=5.0.0,<6.0.0',
 'qctrl>=22.0.0,<23.0.0']

setup_kwargs = {
    'name': 'qctrl-experiment-scheduler',
    'version': '0.2.0',
    'description': 'Q-CTRL Experiment Scheduler',
    'long_description': '# Q-CTRL Experiment Scheduler\n\nThe Q-CTRL Experiment Scheduler provides convenience functionality to use\nQ-CTRL software in a series of interdependent calibration experiments.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
