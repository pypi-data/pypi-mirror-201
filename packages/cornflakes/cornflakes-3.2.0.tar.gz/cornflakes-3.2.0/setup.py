# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cornflakes',
 'cornflakes.builder',
 'cornflakes.click',
 'cornflakes.click.options',
 'cornflakes.click.rich',
 'cornflakes.common',
 'cornflakes.decorator',
 'cornflakes.decorator.config',
 'cornflakes.decorator.dataclass',
 'cornflakes.decorator.dataclass.validator',
 'cornflakes.logging',
 'cornflakes.parser']

package_data = \
{'': ['*']}

modules = \
['build']
install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click>=8.1.3,<9.0.0',
 'rich-rst>=1.1.7,<2.0.0',
 'rich>=12.6,<14.0',
 'types-pyyaml>=6.0.12.1,<7.0.0.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['cornflakes = cornflakes.__main__:main']}

setup_kwargs = {
    'name': 'cornflakes',
    'version': '3.2.0',
    'description': 'Create generic any easy way to manage Configs for your project',
    'long_description': '.. image:: https://github.com/semmjon/cornflakes/blob/main/assets/cornflakes.png?raw=true\n   :height: 400 px\n   :width: 400 px\n   :alt: cornflakes logo\n   :align: center\n\n==========\n\n|PyPI| |Python Version| |License| |Read the Docs| |Build| |Tests| |Codecov|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/cornflakes.svg\n   :target: https://pypi.org/project/cornflakes/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/cornflakes\n   :target: https://pypi.org/project/cornflakes\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/semmjon/cornflakes\n   :target: https://opensource.org/licenses/Apache2.0\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/cornflakes/latest.svg?label=Read%20the%20Docs\n   :target: https://cornflakes.readthedocs.io\n   :alt: Read the documentation at https://cornflakes.readthedocs.io\n.. |Build| image:: https://github.com/semmjon/cornflakes/workflows/Build%20cornflakes%20Package/badge.svg\n   :target: https://github.com/semmjon/cornflakes/actions?workflow=Package\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/semmjon/cornflakes/workflows/Run%20cornflakes%20Tests/badge.svg\n   :target: https://github.com/semmjon/cornflakes/actions?workflow=Tests\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/semmjon/cornflakes/branch/release-1.4.5/graph/badge.svg\n   :target: https://codecov.io/gh/semmjon/cornflakes\n   :alt: Codecov\n\n.. code::\n\n   pip install cornflakes\n\n.. code::\n\n    pip install git+https://github.com/semmjon/cornflakes\n\nInformation\n-----------\n\nThis package was created by starting C ++ methods to incorporate into my python implementations.\nTo make things easier for me, lightweight public libraries were included\n(especially to carry out string operations):\n\n* hash-library\n* strtk\n* rapidjson\n\nFeatures:\n~~~~~~~~~\n\nThe following features have currently been implemented:\n    * config management system\n        - based on dataclass\n        - alternative Implementation for pydantic (BaseSettings)\n        - ini support files by a lightweight and fast parser (-> ini_load)\n        - yaml support (based on PyYAML)\n        - environment variables\n        - (future) support json (based on orjson)\n    * command line interface management\n        - method: click_cli (decorator)\n        - based on click and rich\n        - easy to use and start with\n    * eval_type\n        - method to parse strings in python-types e.g. int | bool | timestamp\n    * simple_hmac\n        - vectorized c++ hmac implementation\n    * default_ca_path\n        - python function to find a default ssl / ca certificate path\n\nCurrently, the package is tested for Linux, Mac and Windows\n\nDevelopment\n-----------\n\nPrerequisites\n~~~~~~~~~~~~~\n\n-  A compiler with C++17 support\n-  Pip 10+ or CMake >= 3.4 (or 3.8+ on Windows, which was the first version to support VS 2015)\n-  Python 3.8+\n-  doxygen\n-  cppcheck\n-  clang-tools-extra or clang-tidy\n-  ..\n\nCommands\n~~~~~~~~~~~~\n\nJust clone this repository and pip install. Note the ``--recursive``\noption which is needed for the pybind11 submodule:\n\n.. code::\n\n   git clone --recursive https://gitlab.blubblub.tech/sgeist/cornflakes.git\n\nInstall the package using makefiles:\n\n.. code::\n\n   make install\n\nBuild dist using makefiles:\n\n.. code::\n\n   make dist\n\nRun tests (pytest) using makefiles:\n\n.. code::\n\n   make test\n\n\nRun all tests using makefiles:\n\n.. code::\n\n   make test-all\n\nRun lint using makefiles:\n\n.. code::\n\n   make lint\n\nCreate dev venv:\n\n.. code::\n\n   python -m venv .venv\n   source .venv/bin/activate\n   pip install cookietemple ninja pre-commit poetry\n\nBump Version using cookietemple:\n\n.. code::\n\n   cookietemple bump-version "<version(e.g 0.0.1)>"\n\nRun lint using cookietemple:\n\n.. code::\n\n   cookietemple lint .\n\nInstall pre-commit:\n\n.. code::\n\n   pre-commit install\n\nUpdate pre-commit:\n\n.. code::\n\n   pre-commit update -a\n\nRun pre-commit:\n\n.. code::\n\n   pre-commit run -a\n\nPublish\n~~~~~~~\n\nIts not recommended publish manually (use git-ci or github workflows instead).\n\n.. code::\n\n   make publish\n',
    'author': 'Semjon Geist',
    'author_email': 'semjon.geist@ionos.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sgeist/cornflakes',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
