# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['droombot']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.4,<4.0.0',
 'aiolimiter>=1.0.0,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'py-cord[speed]>=2.4.1,<3.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'redis[hiredis]>=4.5.4,<5.0.0']

entry_points = \
{'console_scripts': ['droombot = droombot.cli:cli']}

setup_kwargs = {
    'name': 'droombot',
    'version': '0.1.0',
    'description': 'A Discord Bot for generating images from text prompts',
    'long_description': '# Droombot\n\nDroombot is a discord bot for generating images from text prompts.\n\nAt current, it uses an API call to Stability.ai to generate images.\nA future version may support running Stable Diffusion directly.\n\n## Installing\n\n:zap: Note: this step is not necessary if using a Container (see below)\n\nRun the following, preferably in a virtual environment, to install droombot\n\n```console\npip install droombot\n```\n\n## How to run\n\n:zap: Note: this step is not necessary if using a Container (see below)\n\nConfigure your environment (see configuration options below), and make sure a\nredis instance is running on your network (we recommend using a container).\n\nTo start the bot, run the following in the virtual environment:\n\n```console\ndroombot server\n```\n\nTo start a worker, run the following in the virtual environment\n\n```console\ndroombot worker\n```\n\n## Components\n\nDroombot consists of two components:\n\n1. The `server`, this handles interaction with the user. I.e., it handles incoming\n   prompts and replies. It provides the Discord bot users interact with.\n2. One or more `worker`s. These handle the actual image generation.\n\nRedis is used as a message broker between the `server` and the `worker`(s).\n\n## Configuration\n\nAll configuration is handled via environment variables. See the following table\n\n| Environment variable      | Description                                                                    | Is Required               |\n|---------------------------|--------------------------------------------------------------------------------|---------------------------|\n| `DISCORD_BOT_TOKEN`       | Token for your discord application                                             | Yes                       |\n| `DISCORD_GUILD_IDS`       | Comma-separated list of guild (server) ids you want to allow access to the bot | Yes                       |\n| `STABILITY_API_KEY`       | API key from Stability AI                                                      | Yes                       |\n| `REDIS_HOST`              | Hostname of Redis instance                                                     | No, defaults to localhost |\n| `REDIS_PORT`              | Port of Redis instance                                                         | No, defaults to 6379      |\n| `REDIS_KEY_LIFETIME`      | Number of seconds for keys to expire                                           | No, defaults to 300       |\n| `MAX_REQUESTS_PER_MINUTE` | Maximum number of requests per minute to any remote services                   | No, defaults to 100       |\n\n\n## Container\n\nDroombot can run as a container. For a howto using Docker or Podman, see the \n[container docs](docs/containers.md).\n\n## Future plans\n\n1. Expose additional options, such as multiple images and model selection.\n2. Ability to run Stable Diffusion directly, with a separate worker class\n3. Prompt translations, allowing users to use prompts in their own language.\n',
    'author': 'Sander Bollen',
    'author_email': 'sander@sndrtj.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sndrtj/droombot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
