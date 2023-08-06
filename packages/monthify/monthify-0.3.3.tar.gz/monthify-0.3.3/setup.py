# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monthify']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'cachetools>=5.2.1,<6.0.0',
 'loguru>=0.6.0,<0.7.0',
 'rich>=13.1.0,<14.0.0',
 'spotipy>=2.22.0,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['monthify = monthify.main:run']}

setup_kwargs = {
    'name': 'monthify',
    'version': '0.3.3',
    'description': 'Sorts liked spotify tracks into playlists by the month they were liked.',
    'long_description': '# Monthify\n\nA python script that sorts the user\'s liked Spotify tracks into playlists by the month they were liked.\nInspired by an [IFTTT applet](https://ifttt.com/applets/rC5QtGu6-add-saved-songs-to-a-monthly-playlist) by user [t00r](https://ifttt.com/p/t00r)\n\n## Requirements\n\n- Python 3.10+\n- A spotify account\n- [Spotify Client_id and Client_secret](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)\n\n## Install\n\n```\npip install monthify\n```\n\n## Usage\n\n```\nmonthify --client-id=CLIENT_ID --client-secret=CLIENT_SECRET --options\n```\n\nOr with a configuration file\n\n```\nmonthify --options\n```\n\n## Configuration\n\nMonthify will look for a monthify.toml file in\n\nLinux\n\n```\n~/.config/monthify/\n```\n\nWindows\n\n```\nC:\\Users\\username\\AppData\\Local\\Monthify\n```\n\nMac OS\n\n```\n/Users/username/Library/Application Support/Monthify\n```\n\n<br>\nYour monthify.toml file should look like this\n\n```toml\nCLIENT_SECRET="..."\nCLIENT_ID="..."\n```\n\n## Building\n\n### Required\n\n- [Poetry](https://python-poetry.org)\n\n```\ngit clone https://github.com/madstone0-0/monthify.git\ncd monthify\npoetry install\npoetry build\n```\n',
    'author': 'Madiba Hudson-Quansah',
    'author_email': 'mhquansah@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
