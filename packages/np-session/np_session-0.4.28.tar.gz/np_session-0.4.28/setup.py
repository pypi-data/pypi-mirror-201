# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_session',
 'np_session.components',
 'np_session.databases',
 'np_session.jobs']

package_data = \
{'': ['*']}

install_requires = \
['backports.cached-property',
 'firebase-admin>=6.1.0,<7.0.0',
 'np_config>=0.4.17',
 'np_logging>=0.3.8',
 'psycopg2-binary>=2,<3',
 'pydantic>=1.10.5,<2.0.0',
 'redis>=4.5.1,<5.0.0',
 'requests>=2,<3',
 'typing-extensions>=4']

setup_kwargs = {
    'name': 'np-session',
    'version': '0.4.28',
    'description': 'Tools for accessing data, metadata, and jobs related to ecephys and behavior sessions for the Mindscope Neuropixels team.',
    'long_description': "# np_session\n\n\n### *For use on internal Allen Institute network*\n\n\n```python\n>>> from np_session import Session\n\n# initialize with a lims session ID or a string containing one: \n>>> session = Session('c:/1116941914_surface-image1-left.png') \n>>> session.lims.id\n1116941914\n>>> session.folder\n'1116941914_576323_20210721'\n>>> session.is_ecephys_session\nTrue\n>>> session.rig.acq # hostnames reflect the computers used during the session, not necessarily the current machines\n'W10DT05515'\n\n# some properties are objects with richer information:\n>>> session.mouse\nMouse(576323)\n>>> session.project\nProject('NeuropixelVisualBehavior')\n\n# - `pathlib` objects for filesystem paths:\n>>> session.lims_path.as_posix()\n'//allen/programs/braintv/production/visualbehavior/prod0/specimen_1098595957/ecephys_session_1116941914'\n>>> session.data_dict['es_id']\n'1116941914'\n\n# - `datetime` objects for easy date manipulation:\n>>> session.date\ndatetime.date(2021, 7, 21)\n\n# - dictionaries from lims (loaded lazily):\n>>> session.mouse.lims\nLIMS2MouseInfo(576323)\n>>> session.mouse.lims.id\n1098595957\n>>> session.mouse.lims['full_genotype']\n'wt/wt'\n\n# with useful string representations:\n>>> str(session.mouse)\n'576323'\n>>> str(session.project)\n'NeuropixelVisualBehavior'\n>>> str(session.rig)        # from `np_config` package\n'NP.0'\n\n```\n",
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
