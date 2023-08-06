# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teller_cli',
 'teller_cli.core',
 'teller_cli.core.utils',
 'teller_cli.core.world']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0',
 'keyring>=23.13.1,<24.0.0',
 'nanoid-dictionary>=2.4.0,<3.0.0',
 'nanoid>=2.0.0,<3.0.0',
 'nbtlib>=2.0.4,<3.0.0',
 'prompt-toolkit>=3.0.38,<4.0.0',
 'python-slugify>=8.0.1,<9.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['teller-cli = teller_cli:app']}

setup_kwargs = {
    'name': 'teller-cli',
    'version': '0.3.9',
    'description': '',
    'long_description': '# Teller-CLI for ChunkVault-Lite\n\nTeller-CLI is an open source Python/Typer-based CLI tool for uploading Minecraft world backups to ChunkVault-Lite, an open source backup solution provided by Valink Solutions.\n\n## Testing\n\nLimited testing was done on MacOS 13 and Windows 10\n\n## Usage\n\nTo use Teller-CLI, first install the tool:\n\n```bash\n    pip install teller-cli\n```\n\nThen, run the following command to create a snapshot:\n\n```bash\n    teller-cli upload "/path/to/world"\n```\n\nThis will upload the specified backup to ChunkVault-Lite.\n\n### First Launch\n\nOn first launch, Teller-CLI will prompt you to enter the API URL for your ChunkVault-Lite instance. The trailing slash is not necessary, so you can enter the URL without it.\n\nAfter entering the API URL, Teller-CLI will prompt you to enter your API token. You can obtain this token from your ChunkVault-Lite instance. This token is required for authentication purposes and allows Teller-CLI to access your backups.\n\nOnce you have entered the API URL and token, Teller-CLI will store this information locally for future use. You can update this information at any time by running the `teller-cli config` command.\n\n---\n\n## Additional Information\n\nChunkVault-Lite is hosted in a separatly. For more information on ChunkVault-Lite visit the [Repository](https://github.com/Valink-Solutions/ChunkVault-Lite)\n',
    'author': 'JakePIXL',
    'author_email': 'jakewjevans@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
