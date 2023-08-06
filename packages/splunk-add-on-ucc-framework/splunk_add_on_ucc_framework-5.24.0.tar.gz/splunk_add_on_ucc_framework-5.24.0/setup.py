# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunk_add_on_ucc_framework',
 'splunk_add_on_ucc_framework.commands',
 'splunk_add_on_ucc_framework.commands.init_template.{{cookiecutter.addon_name}}.package.bin',
 'splunk_add_on_ucc_framework.commands.modular_alert_builder',
 'splunk_add_on_ucc_framework.commands.openapi_generator',
 'splunk_add_on_ucc_framework.commands.rest_builder',
 'splunk_add_on_ucc_framework.commands.rest_builder.endpoint']

package_data = \
{'': ['*'],
 'splunk_add_on_ucc_framework': ['package/appserver/static/js/*',
                                 'package/appserver/static/js/build/*',
                                 'package/appserver/templates/*',
                                 'package/default/data/ui/nav/*',
                                 'package/default/data/ui/views/*',
                                 'schema/*',
                                 'static/*',
                                 'templates/*'],
 'splunk_add_on_ucc_framework.commands': ['init_template/*',
                                          'init_template/{{cookiecutter.addon_name}}/*',
                                          'init_template/{{cookiecutter.addon_name}}/package/*',
                                          'init_template/{{cookiecutter.addon_name}}/package/lib/*'],
 'splunk_add_on_ucc_framework.commands.modular_alert_builder': ['arf_template/*',
                                                                'arf_template/default_html_theme/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'addonfactory-splunk-conf-parser-lib>=0.3.3,<0.4.0',
 'cookiecutter>=2.1.1,<3.0.0',
 'dunamai>=1.9.0,<2.0.0',
 'jinja2>=2,<4',
 'jsonschema>=4.4.0,<5.0.0',
 'openapi3>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['ucc-gen = splunk_add_on_ucc_framework.main:main']}

setup_kwargs = {
    'name': 'splunk-add-on-ucc-framework',
    'version': '5.24.0',
    'description': 'Splunk Add-on SDK formerly UCC is a build and code generation framework',
    'long_description': "# splunk-add-on-ucc-framework\n\n![PyPI](https://img.shields.io/pypi/v/splunk-add-on-ucc-framework)\n![Python](https://img.shields.io/pypi/pyversions/splunk-add-on-ucc-framework.svg)\n\n## What is UCC?\n\nUCC stands for  Universal Configuration Console. It is a service for generating Splunk Add-ons which is easily customizable and flexible.\nUCC provides basic UI template for creating Addon's UI. It is helpful to control the activity by using hooks and other functionalities.\n\n## Usage\n\nFor full usage instructions, please visit the [documentation](https://splunk.github.io/addonfactory-ucc-generator/).\n\n## Communication channels\n\nIf you are a Splunker use: https://splunk.slack.com/archives/C03T8QCHBTJ\n\nIf you are a part of the community use: https://splunk-usergroups.slack.com/archives/C03SG3ZL4S1\n\n## Contributing Guidelines\n\nGo to [Contributing Guidelines](https://splunk.github.io/addonfactory-ucc-generator/contributing/).\n",
    'author': 'Splunk',
    'author_email': 'addonfactory@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/splunk/addonfactory-ucc-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
