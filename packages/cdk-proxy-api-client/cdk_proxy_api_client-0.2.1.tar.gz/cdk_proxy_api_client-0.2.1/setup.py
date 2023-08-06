# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdk_proxy_api_client',
 'cdk_proxy_api_client.admin_auth',
 'cdk_proxy_api_client.cli',
 'cdk_proxy_api_client.common',
 'cdk_proxy_api_client.models',
 'cdk_proxy_api_client.specs',
 'cdk_proxy_api_client.tenant_mappings',
 'cdk_proxy_api_client.tools']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

extras_require = \
{'cli': ['jsonschema>=4.17.3,<5.0.0',
         'compose-x-common>=1.2,<2.0',
         'importlib-resources>=5.12.0,<6.0.0'],
 'tools': ['jsonschema>=4.17.3,<5.0.0',
           'compose-x-common>=1.2,<2.0',
           'importlib-resources>=5.12.0,<6.0.0']}

entry_points = \
{'console_scripts': ['cdk-cli = cdk_proxy_api_client.cli:main']}

setup_kwargs = {
    'name': 'cdk-proxy-api-client',
    'version': '0.2.1',
    'description': 'Conduktor Proxy API Client',
    'long_description': '# cdk-proxy-api-client\n\nAPI Client library to interact with Conduktor Proxy\n\nCurrent version: v1beta1\n\n\n## Getting started\n\nFirst, create a Proxy Client\n\n```python\nfrom cdk_proxy_api_client.proxy_api import ApiClient, ProxyClient\n\napi = ApiClient("localhost", port=8888, username="superUser", password="superUser")\nproxy_client = ProxyClient(api)\n```\n\n### Features\n\nNote: we assume you are re-using the ``proxy_client`` as shown above.\n\n* Create new Token for a tenant\n\n```python\nfrom cdk_proxy_api_client.admin_auth import AdminAuth\n\nadmin = AdminAuth(proxy_client)\nadmin.create_tenant_credentials("a_tenant_name")\n```\n\n* List all topic mappings for a tenant\n\n```python\nfrom cdk_proxy_api_client.proxy_api import Multitenancy\n\ntenants_mgmt = Multitenancy(proxy_client)\ntenants = tenants_mgmt.list_tenants(as_list=True)\n```\n\n* Create a new mapping for a tenant\n* Delete a tenant - topic mapping\n* Delete all topic mappings for a tenant\n\n```python\nfrom cdk_proxy_api_client.tenant_mappings import TenantTopicMappings\n\ntenant_mappings_mgmt = TenantTopicMappings(proxy_client)\ntenant_mappings_mgmt.create_tenant_topic_mapping(\n    "tenant_name", "logical_name", "real_name"\n)\ntenant_mappings_mgmt.delete_tenant_topic_mapping("tenant_name", "logical_name")\n```\n\n## Testing\nThe testing is for now very manual. See ``e2e_testing.py``\n\nPytest will be added later on\n\n\n## Tools & CLI\n\nTo simplify the usage of the client, you can use some CLI commands\n\n```shell\nusage: CDK Proxy CLI [-h] [--format OUTPUT_FORMAT] --username USERNAME --password PASSWORD --url URL {auth,tenant-topic-mappings,tenants} ...\n\npositional arguments:\n  {auth,tenant-topic-mappings,tenants}\n                        Resources to manage\n    auth                Manages proxy tenant token\n    tenant-topic-mappings\n                        Manages tenant mappings\n    tenants             Manage tenants\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --format OUTPUT_FORMAT, --output-format OUTPUT_FORMAT\n                        output format\n  --username USERNAME\n  --password PASSWORD\n  --url URL\n\n```\n\n### cdk-cli tenant-topic-mappings\n\n```shell\nusage: CDK Proxy CLI tenant-topic-mappings [-h] {list,create,import-from-tenants-config,import-from-tenant,delete-all-mappings,delete-topic-mapping} ...\n\npositional arguments:\n  {list,create,import-from-tenants-config,import-from-tenant,delete-all-mappings,delete-topic-mapping}\n                        Mappings management\n    list                List tenant mappings\n    create              Create a new tenant mapping\n    import-from-tenants-config\n                        Create topic mappings from existing tenants\n    import-from-tenant  Import all topics from a existing tenant\n    delete-all-mappings\n                        Delete all topics mappings for a given tenant\n    delete-topic-mapping\n                        Delete a topic mapping for a given tenant\n\noptional arguments:\n  -h, --help            show this help message and exit\n```\n\n#### import-from-tenants-config\n\nThis command uses a configuration file that will be used to propagate mappings from one/multiple existing tenants to another.\n\nexample file:\n\n```yaml\n---\n# example.config.yaml\n\ntenant_name: application-01\nignore_duplicates_conflict: true\nmappings:\n  - logicalTopicName: data.stock\n    physicalTopicName: data.stock\n    readOnly: true\n```\n\n```shell\ncdk-cli --username ${PROXY_USERNAME} \\\n        --password ${PROXY_PASSWORD} \\\n        --url ${PROXY_URL} \\\n        tenant-topic-mappings import-from-tenants-config -f example.config.yaml\n```\n\n### cdk-cli auth\n\n```shell\ncdk-cli auth --help\nusage: CDK Proxy CLI auth [-h] {create} ...\n\npositional arguments:\n  {create}    Token actions to execute\n    create    Create a new tenant proxy JWT Token\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n\n#### cdk-cli-create-tenant-token\n\nCreate a new user tenant token\n\n```shell\ncdk-cli \\\n        --username ${PROXY_USERNAME} \\\n        --password ${PROXY_PASSWORD} \\\n        --url ${PROXY_URL} \\\n        auth create \\\n        --lifetime-in-seconds 3600  \\\n        --tenant-name js-fin-panther-stg\n```\n\n### cdk-cli tenants\n\nManage tenants\n\n```shell\ncdk-cli tenants --help\nusage: CDK Proxy CLI tenants [-h] {list} ...\n\npositional arguments:\n  {list}      Manage tenants\n    list      List tenants\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n',
    'author': 'John "Preston" Mille',
    'author_email': 'john@ews-network.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
