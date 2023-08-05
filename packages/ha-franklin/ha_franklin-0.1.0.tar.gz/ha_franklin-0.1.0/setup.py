# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ha_franklin']

package_data = \
{'': ['*']}

install_requires = \
['ha-mqtt-discoverable>=0.8.1,<0.9.0',
 'pyaml>=21.10.1,<22.0.0',
 'shell>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['ha-cupsd-check-printer = '
                     'ha_franklin.cli:check_cupsd_single_queue_status_app',
                     'ha-cupsd-info = ha_franklin.cli:app_summary',
                     'ha-cupsd-monitor = '
                     'ha_franklin.cli:monitor_cupsd_queue_app',
                     'ha-cupsd-monitor-queues = '
                     'ha_franklin.cli:monitor_cupsd_queue_app',
                     'ha-cupsd-monitor-single-queue = '
                     'ha_franklin.cli:monitor_single_cupsd_queue_app',
                     'ha-cupsd-monitor-version = ha_franklin.cli:app_version',
                     'ha-cupsd-version = ha_franklin.cli:app_version']}

setup_kwargs = {
    'name': 'ha-franklin',
    'version': '0.1.0',
    'description': 'ha-franklin monitors CUPSD queues and writes information to MQTT for Home Assistant',
    'long_description': '\n# ha-franklin\n\n[![License](https://img.shields.io/github/license/unixorn/ha-franklin.svg)](https://opensource.org/license/apache-2-0/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/unixorn/ha-franklin/main.svg)](https://github.com/unixorn/ha-franklin)\n[![Downloads](https://static.pepy.tech/badge/ha-franklin)](https://pepy.tech/project/ha-franklin)\n\n<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON\'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n## Table of Contents\n\n- [Background](#background)\n- [Usage](#usage)\n  - [Configuration](#configuration)\n  - [Running the Monitor](#running-the-monitor)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\n## Background\n\nI wanted a non-toy test example of using [ha-mqtt-discoverable](https://github.com/unixorn/ha-mqtt-discoverable/tree/v0.8.1).\n\n`ha-franklin` will monitor CUPSD print queues, and present a binary sensor to Home Assistant over MQTT showing whether the printer is printing.\n\nI use this to turn the smart switch for the HP 4050N in the basement on and off so that by the time I walk downstairs from my office after printing something, Home Assistant has turned on the power to the printer and the job has started printing.\n\n\n## Usage\n\n### Configuration\n\nCreate a config file (yaml) with a list of dictionaries in it. Each dictionary should have the following keys:\n- `mqtt_server`: DNS name or a raw IP.\n- `mqtt_user`: the_mqtt_user\n- `mqtt_password`: the_mqtt_password\n- `name`: Franklin@cupsd\n- `unique_id`: printername-cupsd\n- `cupsd_queue_name`: Queue_name_on_cupsd_server\n- `cupsd_server`: cupsd.example.com\n- `check_interval`: 10\n\nThe easiest way to create a configuration file is to start by copying `config/config-example.yaml` and editing it to fit.\n\n### Running the Monitor\n\nI recommend using `docker`, `nerdctl` or `podman` to run the tooling in a container.\n\n`docker run -v "$(pwd)/config":/config --rm unixorn/ha-franklin ha-cupsd-monitor-queues --settings-file /config/config.yaml`\n',
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<4.0',
}


setup(**setup_kwargs)
