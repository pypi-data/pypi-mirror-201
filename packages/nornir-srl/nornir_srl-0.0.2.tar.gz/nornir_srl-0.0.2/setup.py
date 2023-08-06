# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_srl', 'nornir_srl.connections', 'nornir_srl.tasks']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'deepdiff>=6.2.1,<7.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'jsondiff>=2.0.0,<3.0.0',
 'natsort>=8.2.0,<9.0.0',
 'nornir-jinja2>=0.2.0,<0.3.0',
 'nornir-scrapli>=2022.1.30,<2023.0.0',
 'nornir-utils>=0.2.0,<0.3.0',
 'nornir>=3.3.0,<4.0.0',
 'pygnmi>=0.8.9,<0.9.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['fcli = nornir_srl.fsc:cli'],
 'nornir.plugins.connections': ['srlinux = '
                                'nornir_srl.connections.srlinux:SrLinux']}

setup_kwargs = {
    'name': 'nornir-srl',
    'version': '0.0.2',
    'description': 'Nornir connection plugin for SRLinux',
    'long_description': '# nornir_srl\nThis module provides a [Nornir](https://nornir.readthedocs.io/en/latest/) connection [plugin](https://nornir.tech/nornir/plugins/) for Nokia SRLinux devices. It uses the gNMI management interface of SRLinux to fetch state and push configurations.\n\nThe current functionality is focused on a read-only _network-wide CLI_ to perform show commands across an entire set or subset for SRLinux nodes, as defined in the Nornir inventory and through command-line filter options. It shows output in a tabular format for easy reading.\nFollowing versions will focus on configuration management and command execution on the nodes.\n\n# Prerequisites\n\nThis module requires [Nornir Core](https://github.com/nornir-automation/nornir) that includes the Nornir core components for which this module is an add-on.\nNornir needs a [configuration file](https://nornir.readthedocs.io/en/latest/configuration/index.html) to tell it at a minimum where to find the inventory and what inventory plugin is used. Also runner configuration parameters, like #threads/workers for parallel execution are defined here but sane defaults are used.\n\nSince this module is using gNMI as the management inteface, at a minimum, a CA certificate is required that was used to create per-device certs and keys. If you use [Containerlab](https://containerlab.dev/) this root cert is auto-generated for SRLinux nodes and available in the lab subfolder created by the containerlab cli. This file needs to be referenced via the inventory (per-device or per-group). See below for details.\n\n# Installation\n\nCreate a Python virtual-env using your favorite workflow, For example:\n```\npython3 -m venv .venv\nsource .venv/bin/activate\n```\nFollowing command will install the the `nornir_srl` module and all its dependencies, including Nornir core.\n\n```\npip install nornir_srl\n```\nCreate the Nornir confguration file, for example:\n\n```yaml\n# nornir_config.yaml\ninventory:\n    #    plugin: SimpleInventory\n    plugin: YAMLInventory\n    options:\n        host_file: "./inventory/hosts.yaml"\n        group_file: "./inventory/groups.yaml"\n        defaults_file: "./inventory/defaults.yaml"\nrunner:\n    plugin: threaded\n    options:\n        num_workers: 20\n```\nCreate the inventory files as referenced in the above configuration file, for example:\n```yaml\n## hosts.yaml\nclab-4l2s-l1:\n    hostname: clab-4l2s-l1\n    groups: [srl, fabric, leafs]\nclab-4l2s-l2:\n    hostname: clab-4l2s-l2\n    groups: [srl, fabric, leafs]\nclab-4l2s-s1:\n    hostname: clab-4l2s-s1\n    groups: [srl, fabric, spines]\n```\n\n```yaml\n## groups.yaml\nglobal:\n    data:\n        domain: clab\nsrl:\n    connection_options:\n        srlinux:\n            port: 57400\n            username: admin\n            password: admin\n            extras:\n                path_cert: "./root-ca.pem"\nspines:\n    groups: [ global ]\n    data:\n        role: spine\n        type: ixr-d3\nleafs:\n    groups: [ global ]\n    data:\n        role: leaf\n        type: ixr-d2\n```\nThe root certificate is specified once for all devices in group `srl` via the `connection_options.srlinux.extras.path_cert` parameter.\n\n# Use\n\nCurrently, only the network-wide cli functionality is supported via the `fcli` command\n```\nfcli --help\nUsage: fcli [OPTIONS] REPORT\n\nOptions:\n  -c, --cfg TEXT           Nornir config file  [default: nornir_config.yaml]\n  -i, --inv-filter TEXT    filter inventory, e.g. -i site=lab -i role=leaf\n  -f, --field-filter TEXT  filter fields, e.g. -f state=up -f\n                           admin_state=enable\n  --help                   Show this message and exit.\n  ```\n  `REPORT` is a mandatory argument and specifies the report to run. To know which reports are supported, specify a dummy report name:\n```\n  fcli test\nReport test not found. Available reports: [\'bgp-peers\', \'subinterface\', \'ipv4-rib\', \'mac-table\', \'sys-info\', \'nwi-itfs\', \'lldp-nbrs\']\n```\nThe nornir configuration file (`-c` option) is mandatory for nornir to find the inventory files.\nOptionally, you can specify filters to control the output. There are 2 types of filters:\n\n    - inventory filters, specified with the `-i` option, filter on the inventory, e.g. `-i hostname=clab-4l2s-l1`  or `-i role=leaf` based on inventory data\n    - field filters, specified with the `-f` option. This filters based on the fields shown in the report and a value substring, e.g. `-f state=esta`. Multiple field filters can be specified by repeated `-f` options\n\nAn example:\n```\n$ fcli bgp-peers -i role=spine\n                                        BGP Peers                                         \n                               Inventory:{\'role\': \'spine\'}                                \n               ╷          ╷                 ╷         ╷          ╷         ╷              \n  Node         │ NetwInst │ 1_Peer          │ 2_Group │ local_as │ peer_as │ state        \n ══════════════╪══════════╪═════════════════╪═════════╪══════════╪═════════╪═════════════ \n  clab-4l2s-s1 │ default  │ 192.168.0.1     │ leafs   │ [65100]  │ 65001   │ established  \n               │          │ 192.168.0.3     │ leafs   │ [65100]  │ 65002   │ established  \n               │          │ 192.168.0.5     │ leafs   │ [65100]  │ 65003   │ established  \n               │          │ 192.168.0.7     │ leafs   │ [65100]  │ 65004   │ established  \n               │          │ 192.168.0.225   │ dcgw    │ [65100]  │ 65200   │ active       \n               │          │ 192.168.0.227   │ dcgw    │ [65100]  │ 65201   │ active       \n               │          │ 192.168.255.1   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.2   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.3   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.4   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.200 │ overlay │ [100]    │ 100     │ connect      \n               │          │ 192.168.255.201 │ overlay │ [100]    │ 100     │ connect      \n ──────────────┼──────────┼─────────────────┼─────────┼──────────┼─────────┼───────────── \n  clab-4l2s-s2 │ default  │ 192.168.0.229   │ dcgw    │ [65100]  │ 65200   │ active       \n               │          │ 192.168.0.231   │ dcgw    │ [65100]  │ 65201   │ active       \n               │          │ 192.168.1.1     │ leafs   │ [65100]  │ 65001   │ established  \n               │          │ 192.168.1.3     │ leafs   │ [65100]  │ 65002   │ established  \n               │          │ 192.168.1.5     │ leafs   │ [65100]  │ 65003   │ established  \n               │          │ 192.168.1.7     │ leafs   │ [65100]  │ 65004   │ established  \n               │          │ 192.168.255.1   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.2   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.3   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.4   │ overlay │ [100]    │ 100     │ established  \n               │          │ 192.168.255.200 │ overlay │ [100]    │ 100     │ connect     \n```\n\n  \n',
    'author': 'Walter De Smedt',
    'author_email': 'walter.de.smedt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wdesmedt/nornir_srl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
