# Minder Downloader
The minder-downloader module is a Python package that provides a user-friendly interface for interacting with the Minder research portal. This package enables users to easily download datasets from the Minder research portal, as well as upload reports to the platform.

The downloading functionality of the package is straightforward to use. The module handles the authentication and request/response handling, so the user doesn't need to worry about the details of these processes. Once authenticated, users can specify the date range and datasets to download, and the module will return the data as a Pandas DataFrame. This makes it easy to work with the data using Python's powerful data analysis tools.

In addition to downloading data, the minder-downloader module also provides a simple way to upload reports to the Minder research portal. This can be done by providing the path to a file and the HTML address to upload the file to. The module takes care of the uploading process, making it easy to share reports with collaborators or the wider research community.

Overall, the minder-downloader package provides a convenient and streamlined way to interact with the Minder research portal, whether you need to download data or upload reports.

## Installation
You can install minder-downloader using pip:

```bash
pip install minder-downloader
```

## Usage
Here is a simple example of how to use minder-downloader to download data from the Minder research portal:

```python
from datetime import datetime, timedelta
from minder_downloader import MinderDatasetDownload

# Define date range and datasets to download
since = datetime.now() - timedelta(days=7)
until = datetime.now()
datasets = ['example_dataset_1', 'example_dataset_2']

# Create downloader object and download data
downloader = MinderDatasetDownload(since, until, datasets)
data = downloader.download_data()

# Print downloaded data
print(data.head())
```

This will download the specified datasets for the past week and print the first few rows of the resulting DataFrame.

## License
minder-downloader is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
This module was created by Dr Eyal Soreq. If you find it useful, please consider citing it in your research.