# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typer_to_textual']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.3.2,<14.0.0', 'textual>=0.10.1,<0.11.0', 'typer>=0.7.0,<0.8.0']

extras_require = \
{':python_version >= "3.10" and python_version < "4.0"': ['xdotool>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'typer-to-textual',
    'version': '2.4.0',
    'description': '',
    'long_description': '# typer-to-texual\n\n**typer-to-textual** is a TUI developed through the Textual module, which aims to simplify \nthe use of applications. This tool analyzes the help screens of different typer applications and creates \na TUI that allows the user to select the desired commands and options easily and intuitively, without the \nneed to know all available commands and options by heart. In summary, the use of the interactive TUI \nrepresents a major step forward in simplifying the use of typer applications and making them more accessible \nto all users, even the less experienced ones.\n\n## Install\n\nAs a preliminary requirement, you need to install some utility:\n\n**xdotool**. Installs the package via prompt with the command: \'sudo apt-get install xdotool\'\n\nAfter that, you can proceed either via PyPI, or by cloning the repository and install dependencies.\nIf you opt for PyPI, run the following command:\n```bash\n$ pip install typer-to-textual\n```\n\nAfter that, **typer-to-textual** can be run with:\n```bash\n$ python3 -m typer-to-textual [typer_application]\n```\n\nIf you instead opt for the repository, you also need the [Poetry](https://python-poetry.org/) Python package manager.\nOn Debian-like OSes it can be installed with the following command:\n```bash\n$ sudo apt install python3-poetry\n```\nAfter that, run the following commands:\n```bash\n$ git clone https://github.com/palla98/typer-to-textual.git\n```\n\nafter downloading:\n```bash\n$ cd typer-to-textual\n\n$ poetry install\n```\n\nAfter that, **typer-to-textual** can be run with:\n```bash\n$ poetry run ./typer_to_textual.py [typer_application]\n```\n\nse però [typer_application] è \'**python3 -m [nome_modulo]**\' bisogna stare attenti perchè si utlizza\nl\'interprete Python dell\'ambiente virtuale creato da Poetry. Quindi bisogna andare ad installare \n[nome_modulo] nell\'ambiente virtuale altrimenti non viene riconosciuto.\n\noppure semplicemente si può lanciare il comando:\n```bash\npython3 typer_to_textual.py \'python3 -m [nome_modulo]\'\n```\n\nla cosa migliore è andare a creare uno script .sh in modo tale da passare direttamente un eseguibile\nLo si va a creare e salvare nella tua directory bin personale:\n(~/.local/bin/[nome_script].sh):\n```bash\nsudo nano ~/.local/bin/[nome_script].sh\n```\n\n```bash\n#!/bin/bash\n\nOLD_PWD=$PWD\n\ncd path/to/executable\npoetry run ./executable "$@"\ncd $PWD\n```\nIn seguito renderlo eseguibile con questo comando:\n```bash\nsudo chmod +x ~/.local/bin/[nome_script].sh\n```\n\ne poi andare a creare un link simbolico:\n```bash\nsudo ln -s  ~/.local/bin/[nome_script].sh ~/.local/bin/[nome_script]\n```\nDopodichè semplicemente basterà chiamare lo script digitando semplicemente il comando [nome_script]\nda qualsiasi posizione nel terminale.\n\nquindi si potrà usare typer-to-textual anche in questo modo senza avere problemi di ambiente virtuale:\n```bash\npoetry run ./typer_to_textual.py [nome_script]\n```',
    'author': 'palla98',
    'author_email': 'pallaria98@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
