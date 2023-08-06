
import numpy as np
import pandas as pd
import requests
import datetime as dt 
from tqdm import tqdm
from pathlib import Path
import yaml
import time
from functools import wraps



def timer(desc : str = None):  # type: ignore
    """timer is a wrapper decorator to report functions duration
    Args:
        desc (str, optional): [description line to print to sdout]. Defaults to None.
    """
    def wrapper(fun):
        @wraps(fun)
        def wrapped(*fun_args, **fun_kwargs):
            start = time.perf_counter()
            if len(fun_args)>0 and isinstance(fun_args[0], str):
                prefix = f'Finished {desc} {fun_args[0]} in:'
            else:
                prefix = f'Finished {desc} in:'
            out = fun(*fun_args, **fun_kwargs)
            elapsed = time.perf_counter() - start
            dur = f'{np.round(elapsed,1)}'
            print(f"{prefix:<40}{dur:>10} {'seconds':<10}")
            return out
        return wrapped
    return wrapper

def seconds_to_time(seconds):
    """seconds_to_time [summary]

    [extended_summary]

    Args:
        seconds ([type]): [description]

    Returns:
        [type]: [description]
    """
    if pd.isnull(seconds):
        return np.full(3,np.nan)
    else:
        h, m = np.divmod(seconds, 3600)
        m, s = np.divmod(m, 60)
        hms = np.array([h, m, s]).astype(int)
        return hms.T

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

    
def angles_to_time(angles, day=24*60**2):
    """angles_to_time [summary]

    [extended_summary]

    Args:
        angles ([type]): [description]
        day ([type], optional): [description]. Defaults to 24*60**2.

    Returns:
        [type]: [description]
    """
    return seconds_to_time((angles * day) / 360)


class BearerAuth(requests.auth.AuthBase):
    """BearerAuth manages the coupling of a token to requests framework

    Args:
        requests ([type]): [description]
    """
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
    
    
def load_yaml(local_file: str) -> dict :
    """load_yaml loads a yaml file into a dictionary
    """
    with open(local_file, 'r') as yamlfile:        
        return yaml.safe_load(yamlfile)    
    
def date2iso(date: dt.datetime, output_fmt: str ='%Y-%m-%dT%H:%M:%S.%f'):
    """date2iso convert a date string to iso format 
    """
    return date.strftime(output_fmt)+'Z'  



def localize_time(df:pd.DataFrame, factors:list, timezones=None):
    """localize_time control for daylight saving and transform to local time 
    """
    data = []
    if timezones is None:
        timezones = ['Europe/London']
        df['timezone'] = np.repeat('Europe/London', df.shape[0])
    for tz in tqdm(timezones, desc="Processing timezones"):
        _df = df[df.timezone == tz].copy()
        try:
            for factor in tqdm(factors, desc="Processing factors"):
                dt = pd.to_datetime(_df[factor],utc=True).dt.tz_localize(None)
                offset = pd.Series([t.utcoffset() for t in dt.dt.tz_localize(
                    tz, ambiguous=True, nonexistent='shift_forward')], index=dt.index)
                _df[factor] = dt + offset
            data.append(_df)
        except:
            print(tz)
    data = pd.concat(data)
    return data

def rolling_window(a, window:int):
    """rolling_window uses stride_tricks to speed up shift by window 
    """
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    c = np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
    seq = ['>'.join(s) for s in c]
    return seq


def mine_transition(df,value:str,datetime:str='start_date',window:int=1):
    """mine_transition extract transitions across timeseries
    """
    df = df.sort_values(datetime).drop_duplicates().reset_index()
    if not df.empty:
       dur = (df[datetime].shift(-window) - 
              df[datetime]).dt.total_seconds().rename('dur')
       start_date = df[datetime].rename('start_date')
       end_date = df[datetime].shift(-window).rename('end_date')
       source = df[value].rename('source')
       sink = df[value].shift(-window).rename('sink')
       transition = pd.Series(rolling_window(df[value].values,window+1), dtype=object).rename('transition')
       return pd.concat([start_date, end_date, source,sink,transition.reindex(sink.index), dur], axis=1)
    else:
       return pd.DataFrame() 

def str_to_time(time):
    """str_to_time converts time in string format to datetime.time format
    """
    return dt.time(*[int(t) for t in time.split(':')])

   
def time_to_angles(time, day=24*60**2):
    """time_to_angles converts time in datetime.time format format to angles
    """    
    time =  str_to_time(time) if str is type(time) else time
    return 360*(time.hour*60**2+time.minute*60+time.second)/day    


def write_yaml(local_file:str, data:dict):
    """write_yaml writes a dictionary structure into a yaml file

    Args:
        local_file (str): [description]
        data (dict): [description]
    """

    with open(local_file, 'w') as yamlfile:
        yaml.safe_dump(data, yamlfile)

def path_exists(local_file:str):
    """path_exists checks if a file exists in the local filesystem

    [extended_summary]

    Args:
        local_file (str): [description]

    Returns:
        [type]: [description]
    """
    return Path(local_file).exists()        