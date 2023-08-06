# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minder_downloader']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24,<2.0',
 'pandas>=1.5,<2.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'minder-downloader',
    'version': '0.1.4',
    'description': 'The minder-downloader module provides a simple interface for downloading datasets and uploading reports using the Minder research portal.',
    'long_description': "# Minder Downloader\nThe minder-downloader module is a Python package that provides a user-friendly interface for interacting with the Minder research portal. This package enables users to easily download datasets from the Minder research portal, as well as upload reports to the platform.\n\nThe downloading functionality of the package is straightforward to use. The module handles the authentication and request/response handling, so the user doesn't need to worry about the details of these processes. Once authenticated, users can specify the date range and datasets to download, and the module will return the data as a Pandas DataFrame. This makes it easy to work with the data using Python's powerful data analysis tools.\n\nIn addition to downloading data, the minder-downloader module also provides a simple way to upload reports to the Minder research portal. This can be done by providing the path to a file and the HTML address to upload the file to. The module takes care of the uploading process, making it easy to share reports with collaborators or the wider research community.\n\nOverall, the minder-downloader package provides a convenient and streamlined way to interact with the Minder research portal, whether you need to download data or upload reports.\n\n## Installation\nYou can install minder-downloader using pip:\n\n```bash\npip install minder-downloader\n```\n\n## Usage\nHere is a simple example of how to use minder-downloader to download data from the Minder research portal:\n\n```python\nfrom datetime import datetime, timedelta\nfrom minder_downloader import MinderDatasetDownload\n\n# Define date range and datasets to download\nsince = datetime.now() - timedelta(days=7)\nuntil = datetime.now()\ndatasets = ['example_dataset_1', 'example_dataset_2']\n\n# Create downloader object and download data\ndownloader = MinderDatasetDownload(since, until, datasets)\ndata = downloader.download_data()\n\n# Print downloaded data\nprint(data.head())\n```\n\nThis will download the specified datasets for the past week and print the first few rows of the resulting DataFrame.\n\n## License\nminder-downloader is licensed under the MIT License. See the LICENSE file for details.\n\n## Acknowledgements\nThis module was created by Dr Eyal Soreq. If you find it useful, please consider citing it in your research.",
    'author': 'Dr Eyal Soreq',
    'author_email': 'eyal.soreq@ukdri.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
