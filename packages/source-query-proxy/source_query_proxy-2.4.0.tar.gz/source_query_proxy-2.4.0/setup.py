# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['source_query_proxy', 'source_query_proxy.source']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=3.0,<4.0',
 'asyncio_dgram>=2.1.0,<3.0.0',
 'backoff>=2.1.0,<3.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'click>=7.0,<8.0',
 'pid>=2.2,<4.0',
 'pydantic[dotenv]>=1.4,<2.0',
 'pylru>=1.2.0,<2.0.0',
 'pyroute2>=0.7.5,<0.8.0',
 'python-dotenv>=0.10.3,<0.15.0',
 'pyyaml>=6.0,<7.0',
 'sentry-sdk>1.14.0',
 'uvloop>=0.16.0']

entry_points = \
{'console_scripts': ['sqproxy = source_query_proxy.cli:sqproxy']}

setup_kwargs = {
    'name': 'source-query-proxy',
    'version': '2.4.0',
    'description': 'Async proxy for Source Engine Query Protocol',
    'long_description': "\nsource-query-proxy\n==================\n\nMotivation\n----------\n\nBasically Source game-servers works in one thread and can't use more than one core for in-game logic.\nFor example - CS:GO, CS:Source, Left 4 Dead 2, etc.\n\nYes, you can use SourceMod to offload calculations (use threading), but we talking about common game logic.\nE.g. you can try use `DoS Protection extension <https://forums.alliedmods.net/showpost.php?p=2518787&postcount=117>`_, but caching is not fast solution, cause server spent time to receiving and sending answer from cache.\n\nThis solution allow redirect some (A2S query) packets to backend and game server don't spent time to answer anymore.\n\n\nIPTables (or any NAT) can't help!\n---------------------------------\n\nIf you use IPTables (NAT) to redirect queries to proxy, this rule will be remembered in routing table and if client try to connect - connection will be redirected to proxy too.\n\nWe use right way to redirect - eBPF: https://github.com/sqproxy/sqredirect\n\nPrerequisites\n-------------\n\nPython 3.7 or above\n\nYou can use `pyenv <https://github.com/pyenv/pyenv>`_ to install any version of Python without root privileges\n\nInstalling\n----------\n\n.. code-block:: bash\n\n    pip install source-query-proxy==2.4.0\n\nConfiguring\n-----------\n\nsqproxy search configs in ``/etc/sqproxy/conf.d`` and ``./conf.d`` directories.\nYou should place your config files only in this directories.\n\nFor more info see `examples <examples/conf.d>`_\n\nRun\n---\n\n.. code-block:: bash\n\n    sqproxy run\n\n\nRun with eBPF\n-------------\n\nPlease read the instruction and install: https://github.com/sqproxy/sqredirect\n\n1. Enable eBPF in config (see ``examples/00-globals.yaml``)\n\n2. Run\n\n.. code-block:: bash\n\n    sqproxy run\n\nRun daemonized via systemd\n--------------------------\n\n1. Copy the systemd unit file ``examples/systemd/system/sqproxy.service`` to ``/etc/systemd/system/sqproxy.service`` (Optional: Adjust the ``ExecStart`` path if you have installed sqproxy into a different directory)\n\n2. Enable and start the service\n\n.. code-block:: bash\n\n    systemctl enable --now sqproxy.service\n\n\nDevelopment\n-----------\n\n.. code-block:: bash\n\n    git clone https://github.com/spumer/source-query-proxy.git\n    cd source-query-proxy\n    poetry install\n    \n\nCredits\n-------\n\nSource Engine messages inspired by **Python-valve**\nhttps://github.com/serverstf/python-valve\n\n",
    'author': 'spumer',
    'author_email': 'spumer-tm@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sqproxy/sqproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
