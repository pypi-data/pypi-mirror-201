# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['highrise']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4', 'cattrs>=22.2.0,<23.0.0', 'click>=8.1.3']

entry_points = \
{'console_scripts': ['highrise = highrise.__main__:run']}

setup_kwargs = {
    'name': 'highrise-bot-sdk',
    'version': '23.1.0b3',
    'description': 'The Highrise Bot SDK, for running Highrise bots written in Python.',
    'long_description': "# The Highrise Python Bot SDK\n\n---\n\nThe Highrise Python Bot SDK is a python library for writing and running Highrise bots.\n\nFirst, install the library (preferably in a virtual environment):\n\n```shell\n$ pip install highrise-bot-sdk==23.1.0b2\n```\n\nIn the [`Settings` section of the Highrise website](https://highrise.game/account/settings), create a bot and generate the API token. You'll need the token to start your bot later.\nYou will also need a room ID for your bot to connect to; the room needs to be owned by you or your bot user needs to have designer rights to enter it.\n\nOpen a new file, and paste the following to get started (into `mybot.py` for example):\n\n```python\nfrom highrise import BaseBot\n\nclass Bot(BaseBot):\n    pass\n```\n\nOverride methods from `BaseBot` as needed.\n\nWhen you're ready, run the bot from the terminal using the SDK, giving it the Python path to the Bot class:\n\n```\n$ highrise mybot:Bot <room ID> <API token>\n```\n\n## Changelog\n\n### 23.1.0b3 (2023-04-03)\n\n- Fix the chatting API.\n\n### 23.1.0b2 (2023-04-03)\n\n- Add support for receiving and sending reactions.\n- Fix support for hidden channels.\n- Migrate to the new message for avatars leaving.\n- Improve concurrency when awaiting bot methods.\n- Fix issues with teleporting users.\n- Fix issues with user coordinates.\n- Add support for fetching the bot wallet (`self.highrise.get_wallet()`).\n\n### 23.1.0b1 (2023-03-28)\n\n- Add support for emotes and hidden channel messages.\n\n### 23.1.0b0 (2023-03-10)\n\n- Initial beta release.\n",
    'author': 'Pocket Worlds Inc',
    'author_email': 'server@high.rs',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
