# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soundscapy',
 'soundscapy.analysis',
 'soundscapy.databases',
 'soundscapy.plotting',
 'soundscapy.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'acoustics>=0.2.6,<0.3.0',
 'mosqito>=1.0.8,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pyjanitor==0.23.1',
 'pytest>=7.2.2,<8.0.0',
 'scikit-maad>=1.3.12,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'soundscapy',
    'version': '0.4.3',
    'description': 'A python library for analysing and visualising soundscape assessments.',
    'long_description': '<img src="https://raw.githubusercontent.com/MitchellAcoustics/Soundscapy/main/docs/logo/LightLogo.png" width="300">\n\n# Soundscapy\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MitchellAcoustics/Soundscapy/main?labpath=docs%2Ftutorials%2FHowToAnalyseAndRepresentSoundscapes.ipynb)\n\nA python library for analysing and visualising soundscape assessments. \n\n**Disclaimer:** This module is still heavily in development, and might break what you\'re working on. It will also likely require a decent amount of troubleshooting at this stage. I promise bug fixes and cleaning up is coming!\n\n## Installation\n\nThe package is still under development, but can be installed with pip:\n\n```\npip install soundscapy\n```\n\n## Examples\n\nWe are currently working on writing more comprehensive examples and documentation, please bear with us in the meantime. \n\nAn example notebook which reproduces the figures used in our recent paper "How to analyse and represent quantitative soundscape data" is provided in the `examples` folder.\n\n## Acknowledgements\n\nThe newly added Binaural analysis functionality relies directly on three acoustic analysis libraries: \n * [python-acoustics](https://github.com/python-acoustics/python-acoustics) for the standard environmental and building acoustics metrics, \n * [scikit-maad](https://github.com/scikit-maad/scikit-maad) for the bioacoustics and ecological soundscape metrics, and\n * [MoSQITo](https://github.com/Eomys/MoSQITo) for the psychoacoustics metrics. We thank each of these packages for their great work in making advanced acoustic analysis more accessible.\n\n## Citation\n\nIf you are using Soundscapy in your research, please help our scientific visibility by citing our work! Please include a citation to our accompanying paper:\n\nMitchell, A., Aletta, F., & Kang, J. (2022). How to analyse and represent quantitative soundscape data. *JASA Express Letters, 2*, 37201. [https://doi.org/10.1121/10.0009794](https://doi.org/10.1121/10.0009794)\n\n\n<!---\nBibtex:\n```\n@Article{Mitchell2022How,\n  author         = {Mitchell, Andrew and Aletta, Francesco and Kang, Jian},\n  journal        = {JASA Express Letters},\n  title          = {How to analyse and represent quantitative soundscape data},\n  year           = {2022},\n  number         = {3},\n  pages          = {037201},\n  volume         = {2},\n  doi            = {10.1121/10.0009794},\n  eprint         = {https://doi.org/10.1121/10.0009794},\n}\n\n```\n--->\n\n## Development Plans\n\nAs noted, this package is in heavy development to make it more useable, more stable, and to add features and improvements. At this stage it is mostly limited to doing basic quality checks of soundscape survey data and creating the soundscape distribution plots. Some planned improvements are:\n\n - [ ] Simplify the plotting options\n - [ ] Possibly improve how the plots and data are handled - a more OOP approach would be good.\n - [ ] Add appropriate tests and documentation.\n - [ ] Bug fixes, ~~particularly around setting color palettes.~~\n\nLarge planned feature additions are:\n\n - [ ] Add better methods for cleaning datasets, including robust outlier exclusion and imputation.\n - [x] Add handling of .wav files.\n - [x] Integrate environmental acoustic and psychoacoustic batch processing. This will involve using existing packages (e.g. MoSQito, python-acoustics) to do the metric calculations, but adding useful functionality for processing many files at once, tieing them to a specific survey response, and implementing a configuration file for maintaining consistent analysis settings.\n - [ ] Integrate the predictive modelling results from the SSID team\'s research to enable a single pipelined from recording -> psychoacoustics -> predicted soundscape perception (this is very much a pie-in-the-sky future plan, which may not be possible).\n\n### Contributing\n\nIf you would like to contribute or if you have any bugs you have found while using `Soundscapy\', please feel free to get in touch or submit an issue or pull request!\n',
    'author': 'Andrew Mitchell',
    'author_email': 'andrew.mitchell.18@ucl.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MitchellAcoustics/Soundscapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
