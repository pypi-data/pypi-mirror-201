# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rkale']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0', 'tqdm>=4.60.0,<5.0.0']

entry_points = \
{'console_scripts': ['rkale = rkale.rkale:main']}

setup_kwargs = {
    'name': 'rkale',
    'version': '1.0.1',
    'description': 'Rclone wrapper to manage multiple datasets in a project',
    'long_description': '# rkale\n\n## Install\n\nInstall rkale in your project using poetry:\n\n```bash\npoetry add rkale\n```\n\nUse pip if you want a global installation:\n\n```bash\npip install rkale\n```\n\n## Configuration\n\n### Global\n\n`~/.config/rkale/rkale.conf`:\n```toml\n[data]\nroot = "path to data folder where datasets are stored"\n\n[aliases]\nwasabi = "optional alias for remote in rclone.conf"\n\n[rclone] # global flags for rclone\nflags = ["--transfers 32", "--checkers 32"]\n```\n\nIf aliases are empty the remote name from the project config is used in the\nrclone lookup.\n\n### Project\nConfigure project datasets in the pyproject.toml file:\n\n`<project path>/pyproject.toml`:\n```toml\n[[tool.rkale.dataset]]\nname = "dataset_1"\nremote = "remote_1"\n\n[[tool.rkale.dataset]]\nname = "dataset_2"\nremote = "remote_2"\n```\n\nThe remote specified for the dataset must match a remote in the `rclone.conf`\nor an alias in the global rkale configuration.\n\n## Usage\n\n### Python interface\n\n```python\nfrom rkale.config import dataset_paths\n\n\ndef dataset_path():\n    return dataset_paths()["dataset_1"]\n```\n\n### Syncing datasets\n\nSyncs the local datasets to be identical to the remote\n\n```bash\nrkale psync\n```\n\nSyncs the remote datasets to be identical to the local\n\n```bash\nrkale psync --upstream\n```\n\nSame as rclone sync but checks differences first and asks for confirmation\n\n```bash\nrkale sync <source> <destination>\n```\n',
    'author': 'nextml',
    'author_email': 'joar@nextml.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nextml-code/rkale',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
