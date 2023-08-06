# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_client_generator', 'python_client_generator.templates']

package_data = \
{'': ['*']}

install_requires = \
['chevron>=0.14.0,<0.15.0', 'pydantic>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['poetry = poetry.console:main']}

setup_kwargs = {
    'name': 'python-client-generator',
    'version': '1.1.1',
    'description': 'Python package to generate an httpx-based client off an OpenAPI spec',
    'long_description': '# python-client-generator\n\nPython package to generate an [httpx](https://github.com/encode/httpx)- and\n[pydantic](https://github.com/pydantic/pydantic)-based async (or sync) \nclient off an OpenAPI spec.\n\n```mermaid\nflowchart LR\n    generator["python-client-generator"]\n    app["REST API app"]\n    package["app HTTP client"]\n\n    app -- "OpenAPI json" --> generator\n    generator -- "generates" --> package\n```\n\n\n## Using the generator\n\n```bash\npython -m python_client_generator --open-api openapi.json --package-name foo_bar --project-name foo-bar --outdir clients\n```\n\nThis will produce a Python package with the following structure:\n```bash\nclients\n├── foo_bar\n│\xa0\xa0 ├── __init__.py\n│\xa0\xa0 ├── apis.py\n│\xa0\xa0 ├── base_client.py\n│\xa0\xa0 └── models.py\n└── pyproject.toml\n```\n\n### Using PATCH functions from the generator\n\nWhen calling one of the generated update functions that uses an HTTP `PATCH` method, you\'ll\nprobably want to pass the additional argument `body_serializer_args={"exclude_unset": True}`. This\nwill ensure that only the fields that are set in the update object are sent to the API. Example:\n\n```python\nawait api_client.update_contact_v1_contacts__contact_id__patch(\n                body=patch_body,\n                contact_id=contact.id,\n                tenant=tenant,\n                body_serializer_args={"exclude_unset": True}\n)\n```\n\n\n## Contributing\nPlease refer to [CONTRIBUTING.md](.github/CONTRIBUTING.md).\n',
    'author': 'Bogdan Petre',
    'author_email': 'bogdan.petre@sennder.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sennder/python-client-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
