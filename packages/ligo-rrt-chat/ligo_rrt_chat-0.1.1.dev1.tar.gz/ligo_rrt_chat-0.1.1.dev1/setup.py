# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ligo', 'ligo.rrt_chat', 'ligo.rrt_chat.tests']

package_data = \
{'': ['*'], 'ligo.rrt_chat': ['data/*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'safe-netrc>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'ligo-rrt-chat',
    'version': '0.1.1.dev1',
    'description': '',
    'long_description': '# Chat\n\nCreate a mattermost chat for discussing superevents.\n\n## Usage\n\nThis current version uses a superevent_id information\nto make mattermost channels. It only works if the .netrc \nfile has a "mattermost-bot" login with appropiate token as password. \n\nIf the channel creation succeedes, the new channel \nname will be `RRT O4 {superevent_id}`. A post will be \nmade in this channel with a corresponding \ngrace_db url. Raises exceptions in case of failures.\n\n```\nfrom ligo.rrt_chat import channel_creation\nimport json\n\nchannel_creation.rrt_channel_creation(superevent_id, gracedb_url)\n\n```\n',
    'author': 'Sushant Sharma-Chaudhary',
    'author_email': 'sushant.sharma-chaudhary@git.ligo.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
