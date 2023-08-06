# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pysignalr', 'pysignalr.protocol', 'pysignalr.transport']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'msgpack>=1.0.2,<2.0.0', 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'pysignalr',
    'version': '0.2.0',
    'description': 'Modern, reliable and async-ready client for SignalR protocol',
    'long_description': "# pysignalr\n\n[![GitHub stars](https://img.shields.io/github/stars/baking-bad/pysignalr?color=2c2c2c)](https://github.com/baking-bad/pysignalr)\n[![Latest stable release](https://img.shields.io/github/v/release/baking-bad/pysignalr?label=stable%20release&color=2c2c2c)](https://github.com/baking-bad/pysignalr/releases)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysignalr?color=2c2c2c)](https://www.python.org)\n[![License: MIT](https://img.shields.io/github/license/baking-bad/pysignalr?color=2c2c2c)](https://github.com/baking-bad/pysignalr/blob/master/LICENSE)\n<br>\n[![PyPI monthly downloads](https://img.shields.io/pypi/dm/pysignalr?color=2c2c2c)](https://pypi.org/project/pysignalr/)\n[![GitHub issues](https://img.shields.io/github/issues/baking-bad/pysignalr?color=2c2c2c)](https://github.com/baking-bad/pysignalr/issues)\n[![GitHub pull requests](https://img.shields.io/github/issues-pr/baking-bad/pysignalr?color=2c2c2c)](https://github.com/baking-bad/pysignalr/pulls)\n\n**pysignalr** is a modern, reliable, and async-ready client for [SignalR protocol](https://docs.microsoft.com/en-us/aspnet/core/signalr/introduction?view=aspnetcore-5.0). This project started as an asyncio fork of mandrewcito's [signalrcore](https://github.com/mandrewcito/signalrcore) library and ended up as a complete rewrite.\n\n## Usage\n\nLet's connect to [TzKT](https://tzkt.io/), an API and block explorer of Tezos blockchain, and subscribe to all operations:\n\n```python\nimport asyncio\nfrom contextlib import suppress\nfrom typing import Any\nfrom typing import Dict\nfrom typing import List\n\nfrom pysignalr.client import SignalRClient\nfrom pysignalr.messages import CompletionMessage\n\n\nasync def on_open() -> None:\n    print('Connected to the server')\n\n\nasync def on_close() -> None:\n    print('Disconnected from the server')\n\n\nasync def on_message(message: List[Dict[str, Any]]) -> None:\n    print(f'Received message: {message}')\n\n\nasync def on_error(message: CompletionMessage) -> None:\n    print(f'Received error: {message.error}')\n\n\nasync def main() -> None:\n    client = SignalRClient('https://api.tzkt.io/v1/ws')\n\n    client.on_open(on_open)\n    client.on_close(on_close)\n    client.on_error(on_error)\n    client.on('operations', on_message)\n\n    await asyncio.gather(\n        client.run(),\n        client.send('SubscribeToOperations', [{}]),\n    )\n\n\nwith suppress(KeyboardInterrupt, asyncio.CancelledError):\n    asyncio.run(main())\n```\n\n## Roadmap to the stable release\n\n- [ ] More documentation, both internal and user.\n- [ ] Integration tests with containerized ASP hello-world server.\n- [ ] Ensure that authentication works correctly.\n",
    'author': 'Lev Gorodetskii',
    'author_email': 'pysignalr@drsr.io',
    'maintainer': 'Lev Gorodetskii',
    'maintainer_email': 'pysignalr@drsr.io',
    'url': 'https://github.com/baking-bad/pysignalr',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
