# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baserow_open_api_client',
 'baserow_open_api_client.api',
 'baserow_open_api_client.api.admin',
 'baserow_open_api_client.api.applications',
 'baserow_open_api_client.api.audit_log_export',
 'baserow_open_api_client.api.auth',
 'baserow_open_api_client.api.builder_domains',
 'baserow_open_api_client.api.builder_page_elements',
 'baserow_open_api_client.api.builder_pages',
 'baserow_open_api_client.api.database_table_calendar_view',
 'baserow_open_api_client.api.database_table_export',
 'baserow_open_api_client.api.database_table_fields',
 'baserow_open_api_client.api.database_table_form_view',
 'baserow_open_api_client.api.database_table_gallery_view',
 'baserow_open_api_client.api.database_table_grid_view',
 'baserow_open_api_client.api.database_table_kanban_view',
 'baserow_open_api_client.api.database_table_rows',
 'baserow_open_api_client.api.database_table_view_decorations',
 'baserow_open_api_client.api.database_table_view_filters',
 'baserow_open_api_client.api.database_table_view_sortings',
 'baserow_open_api_client.api.database_table_views',
 'baserow_open_api_client.api.database_table_webhooks',
 'baserow_open_api_client.api.database_tables',
 'baserow_open_api_client.api.database_tokens',
 'baserow_open_api_client.api.group_invitations',
 'baserow_open_api_client.api.groups',
 'baserow_open_api_client.api.jobs',
 'baserow_open_api_client.api.role_assignments',
 'baserow_open_api_client.api.settings',
 'baserow_open_api_client.api.snapshots',
 'baserow_open_api_client.api.teams',
 'baserow_open_api_client.api.templates',
 'baserow_open_api_client.api.trash',
 'baserow_open_api_client.api.user',
 'baserow_open_api_client.api.user_files',
 'baserow_open_api_client.api.workspace_invitations',
 'baserow_open_api_client.api.workspaces',
 'baserow_open_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0', 'httpx>=0.15.4,<0.24.0', 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'baserow-open-api-client',
    'version': '0.0.3',
    'description': 'A client library for accessing Baserow OpenAPI',
    'long_description': '# baserow-open-api-client\nA client library for accessing Baserow OpenAPI\n\n## Usage\nFirst, create a client:\n\n```python\nfrom baserow_open_api_client import Client\n\nclient = Client(base_url="https://api.example.com")\n```\n\nIf the endpoints you\'re going to hit require authentication, use `AuthenticatedClient` instead:\n\n```python\nfrom baserow_open_api_client import AuthenticatedClient\n\nclient_which_gets_jwt_using_email_and_pass = AuthenticatedClient(base_url="https://api.example.com", email="your users email", password="your users password")\nclient_given_a_refresh_and_or_access_token = AuthenticatedClient(base_url="https://api.example.com", refresh_token="xyz")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom typing import List\n\nfrom baserow_open_api_client.api.workspaces import list_workspaces\nfrom baserow_open_api_client.client import AuthenticatedClient\nfrom baserow_open_api_client.models import WorkspaceUserWorkspace\nfrom baserow_open_api_client.types import Response\n\n auth_client = AuthenticatedClient("http://localhost:8000", email="dev@baserow.io",\n                                   password="SuperSecretPassword")\n\nresponse: Response[List[WorkspaceUserWorkspace]] = list_workspaces.sync_detailed(\n    client=auth_client)\n```\n\nOr do the same thing with an async version by using the asyncio/asyncio_detailed methods instead.\n```\n\nBy default, when you\'re calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com",\n    refresh_token="SuperSecretToken",\n    verify_ssl="/path/to/certificate_bundle.pem",\n)\n```\n\nYou can also disable certificate validation altogether, but beware that **this is a security risk**.\n\n```python\nclient = AuthenticatedClient(\n    base_url="https://internal_api.example.com",\n    refresh_token="SuperSecretToken",\n    verify_ssl=False\n)\n```\n\nThere are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info.\n\nThings to know:\n1. Every path/method combo becomes a Python module with four functions:\n    1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n    1. `asyncio`: Like `sync` but async instead of blocking\n    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking\n\n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `baserow_open_api_client.api.default`\n\n## Building / publishing this Client\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://baserow.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
