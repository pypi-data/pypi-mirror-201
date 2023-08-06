# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['via_hub_logistc',
 'via_hub_logistc.core',
 'via_hub_logistc.keyword',
 'via_hub_logistc.model']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'via-hub-logistc',
    'version': '0.0.53',
    'description': 'This project is intended to be a facilitator for new developments for test automation',
    'long_description': 'Introduction\n------------\n\nvia-hub-logistic is a library with testing utilities for robotframework that uses a set of python frameworks internally. The project is hosted on GitHub and downloads can be found on PyPI.\n\n\nKeyword Documentation\n---------------------\nSee `keyword documentation`_ for available keywords and more information\nabout the library in general.\n\n\nInstallation\n------------\n\nThe recommended installation method is using pip_::\n\n    pip install --upgrade via-hub-logistc\n\nLib\n-----\n\n\n\nKeywords\n-----\n\nTo use via-hub-logistc in Robot Framework tests, the library needs to\nfirst be imported using the ``Library`` setting as any other library.\nThe library accepts some import time arguments, which are documented\nin the `keyword documentation`_ along with all the keywords provided\nby the library.\n\n.. code:: robotframework report manager\n\n    import           via-hub-logistc.ReportManager\n',
    'author': 'Jaderson Macedo',
    'author_email': 'jaderson.macedo@viavarejo.com.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
