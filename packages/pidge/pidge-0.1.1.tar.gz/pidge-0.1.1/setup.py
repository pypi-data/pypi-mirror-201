# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pidge', 'pidge.tests', 'pidge.tests.fixtures']

package_data = \
{'': ['*'], 'pidge': ['sample_data/fake_expenses.csv']}

install_requires = \
['pandas>=1.5.3,<2.0.0', 'panel>=0.14.4,<0.15.0']

setup_kwargs = {
    'name': 'pidge',
    'version': '0.1.1',
    'description': 'pidge helps with the creation of mappings for tabular string data',
    'long_description': "# pidge\n\npidge helps with the creation of mappings for tabular string data. The primary use cases for\nthis are data cleaning and data categorization.\n\npidge consists out of two parts:\n\n1. An interactive UI to help with the creation of mappings and assessing their completeness\n2. Library functionality to apply mappings inside of data pipelines, after they have been exported from the UI\n\n\n## Usage\n\n1. install `pidge`\n\n        pip install pidge\n\n1. Launch the UI in a notebook\n\n    ```python\n    from pidge import pidge_ui\n    import panel as pn\n\n    pn.extensions('tabulator')\n\n    pidge_ui(my_input_dataframe)\n    ```\n\n1. Create and export a mapping named `pidge_mapping.json`\n\n1. In your data pipeline import `pidge` and apply the mapping\n\n    ```python\n    from pidge import pidge\n\n    transformed_data = pidge(my_input_dataframe,rule_file= 'pidge_mapping.json')\n    ```\n\n### The web-ui outside of Jupyter\n\nPidge can also run the UI as a standalone web server outside of jupyter, using the command.\n\n> python -m pidge\n\nThis starts up the UI in a local web server, which is primarily intended for illustration purposes.\nTherefore it starts up with example data already loaded. However new data can be loaded and the\npredefined rules can easily be reset. The main limitation at this moment, however, is the\nconstraint on the upload format for data. It only supports `.csv` and reads it with default\n`pandas.read_csv` settings.\n\n## Mapping Logic\n\nPidge mappings map a source string column to a newly created target string column. The logic can\nbe broken down as follows.\n\n1. One defines a possible value, a category, for the target column.\n1. One associates one or more patterns with that category.\n1. When a value of the source column matches one of the category's patterns, that category is chosen.\n1. Pattern matching checks whether the pattern is part of the source string. It is case insensitive\n    and allows for regular expressions.\n1. This is repeated for as many categories as desired.\n\n\n## Contribution\n\nPidge is in an early MVP stage. At this stage the following is particularly appreciated\n\n1. Any feedback regarding, bugs, issues usability feature requests etc. Ideally this can be done directly\n    as github issues.\n1. Any sharing of the project to potentially help with the previous point.\n\n## Known Limitations\n\nThere are a few known limitations particularly due to the MVP stage of the project. These\nwill be prioritized according to feedback and general usage of the project.\n\n- Mapping is not optimized for speed at all and might slow down for large dataframes\n- Patterns do not check for multiple inconsistent matches and simply the first applicable pattern\n    is chosen\n- the web-ui does only support small file uploads (around < 10Mb).\n- file uploads can only read in the data with `pandas.read_csv` default settings\n- The rule name used for the .json export can currently not be changed in the UI.\n",
    'author': 'Konrad Wölms',
    'author_email': 'konrad.woelms@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
