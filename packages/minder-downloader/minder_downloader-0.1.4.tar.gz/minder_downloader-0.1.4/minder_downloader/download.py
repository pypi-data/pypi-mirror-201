"""
The `minder` module provides classes and functions for downloading data from the Minder research portal.

Classes:
- MinderDatasetDownload: Class for downloading Minder research portal datasets.

Functions:
- load: Downloads data from the Minder research portal and returns it as a Pandas DataFrame.

Modules:
- utils: Module with utility functions used in this module.
- info: Module with information about available datasets and organizations in the Minder research portal.
- update: Module with functions for updating tokens used to authenticate with the Minder research portal.

Dependencies:
- requests: Library for making HTTP requests.
- json: Library for working with JSON data.
- logging: Library for logging messages.
- pandas: Library for working with tabular data.
- numpy: Library for working with numerical data.
- datetime: Library for working with dates and times.
- tqdm: Library for displaying progress bars.
- os: Library for interacting with the operating system.
- pathlib: Library for working with file paths.
- time: Library for working with time intervals.
- io: Library for working with I/O streams.
- typing: Library for type hinting.

"""



import requests
import json
import logging
import pandas as pd
import numpy as np
import datetime as dt
from tqdm import tqdm
import os
from pathlib import Path
from time import sleep
from io import StringIO
from typing import List,Union
from .utils import BearerAuth, date2iso, load_yaml
from .info import _minder_datasets_info,_minder_organizations_info
from .update import get_token
from .config import check_config

# Set up logging
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)
#
ROOT = os.environ.get('MINDER_DOWNLOADER_HOME', Path(__file__).parent)



class MinderDatasetDownload:
    """
    Class for downloading Minder research portal datasets.

    Methods:
    - __init__: Initializes the object with input parameters.
    - post_request: Sends a POST request to the Minder research portal and stores the resulting request ID.
    - _get_output_urls: Retrieves the output URLs for a previously sent request ID.
    - process_request: Polls the Minder research portal for output URLs until they become available.
    - _persistent_download: Downloads and returns data from a given URL, retrying if necessary.
    - download_data: Downloads data from the Minder research portal and returns it as a Pandas DataFrame.
    """

    def __init__(self, 
                 datasets: List[str],
                 since: Union[dt.datetime, None] = None, 
                 until: Union[dt.datetime, None] = None, 
                 organizations:Union[list, None] = None):
        """
        Initializes the object with input parameters.

        Parameters:
        - since: A datetime object representing the start date of the desired data.
        - until: A datetime object representing the end date of the desired data.
        - datasets: A list of strings representing the names of the datasets to download.
        - organizations (optional): A list of strings representing the names of the organizations to download data from.

        Returns:
        None
        """
        check_config()
        self.setup()        
        since = since or dt.datetime.now() -  dt.timedelta(days=7)
        until = until or dt.datetime.now()
        self.since = date2iso(since)
        self.until = date2iso(until)
        self.datasets = datasets
        self.datasets_info = _minder_datasets_info()
        self.organizations_info = _minder_organizations_info()  
        self.data_request = {
            'since': self.since,
            'until': self.until,
            'datasets': {
                ds: {"columns": self.datasets_info.query('datasets == @ds').availableColumns.iat[0]}
                for ds in self.datasets
            }
        }
        if organizations:
            self.data_request['organizations'] = organizations
        self._request_id = ''
        self._csv_url = pd.DataFrame()

    def setup(self) -> None:
        INFO_PATH = f'{ROOT}{os.sep}info.yaml'
        os.environ['MINDER_TOKEN'] = load_yaml(INFO_PATH)['token']
        self.server = load_yaml(INFO_PATH)['server'] + '/export'
        self.headers = load_yaml(INFO_PATH)['headers'] 
        self.auth = BearerAuth(os.getenv('MINDER_TOKEN'))


    def post_request(self) -> None:
        """
        Sends a POST request to the Minder research portal and stores the resulting request ID.

        Parameters:
        None

        Returns:
        None
        """
        request = requests.post(
            self.server,
            data=json.dumps(self.data_request),
            headers=self.headers,
            auth=self.auth 
        )
        self._request_id = request.headers['Content-Location'].split('/')[-1]
        logging.debug(f"request_id: {self._request_id}")

    def _get_output_urls(self) -> pd.DataFrame:
        """
        Retrieves the output URLs for a previously sent request ID.

        Parameters:
        None

        Returns:
        A Pandas DataFrame with the output URLs and their associated metadata.
        """
        with requests.get(f'{self.server}/{self._request_id}/', auth=self.auth ) as request:
            request_elements = pd.DataFrame(request.json())
            output = pd.DataFrame()
            if request_elements.status.iat[0] == 202:
                logging.debug('*')
            elif request_elements.status.iat[0] == 200:
                if 'output' in request_elements.index:
                    output = pd.DataFrame(request_elements.loc['output'].jobRecord)
                    if output.empty:
                        logging.debug(f'{self._request_id} has no info')
                        output = pd.DataFrame([False])
                    else:
                        logging.debug(f'{self._request_id} received with info')
            else:
                logging.debug(f'Unexpected {request_elements.status.iat[0]} status')
        return output

    def process_request(self, sleep_time: int = 2) -> None:
        """
        Polls the Minder research portal for output URLs until they become available.

        Parameters:
        - sleep_time (optional): An integer representing the number of seconds to wait between polling requests.

        Returns:
        None
        """
        logging.debug(f'Processing {self.datasets}')
        while self._csv_url.empty:
            sleep(sleep_time)
            self._csv_url = self._get_output_urls()
   

    def _persistent_download(self, url: str, idx: int) -> pd.DataFrame:
        """
        Downloads and returns data from a given URL, retrying if necessary.

        Parameters:
        - url: A string representing the URL to download data from.
        - idx: An integer representing the index of the URL in the DataFrame returned by _get_output_urls().

        Returns:
        A Pandas DataFrame with the downloaded data.
        """
        df = pd.DataFrame()
        while df.empty:
            try:
                with requests.get(url, stream=True, auth=self.auth ) as request:
                    decoded_data = StringIO(request.content.decode('utf-8-sig'))
                    df = pd.read_csv(decoded_data, sep=',', engine='python')
                    df['source'] = self._csv_url.type[idx]
            except:
                logging.debug(self._request_id)
            sleep(2)
        return df

    def download_data(self) -> pd.DataFrame:
        """
        Downloads data from the Minder research portal and returns it as a Pandas DataFrame.

        Parameters:
        None

        Returns:
        A Pandas DataFrame with the downloaded data.
        """
        self.post_request()
        self.process_request()

        data = []
        if not self._csv_url.empty and 'url' in self._csv_url:
            for idx, url in enumerate(tqdm(self._csv_url.url,
                                           desc=f'Downloading {self.datasets}',
                                           dynamic_ncols=True)):
                df = self._persistent_download(url, idx)
                data.append(df)
            self.data = pd.concat(data).reset_index(drop=True)
            self.data = self.data[np.any(self.data.values == self.data.columns.values.reshape(1, -1), axis=1) == False]
            self.data = self.data.replace({'false': False, 'true': True})
        else:
            print('No data in this period')
            self.data = pd.DataFrame()
        return self.data
    

    
def load(datasets: list,since: Union[dt.datetime, None] = None, until: Union[dt.datetime, None] = None, organizations: Union[list, None] = None) -> pd.DataFrame:
    """
    Downloads data from the Minder research portal and returns it as a Pandas DataFrame.
    Parameters:
    - since: A datetime object representing the start date of the desired data.
    - until: A datetime object representing the end date of the desired data.
    - datasets: A list of strings representing the names of the datasets to download.
    - organizations (optional): A list of strings representing the names of the organizations to download data from.

    Returns:
    A Pandas DataFrame with the downloaded data.
    """        
    downloader = MinderDatasetDownload(datasets, since, until, organizations)
    downloader.post_request()
    downloader.process_request()
    data = downloader.download_data()
    return data    