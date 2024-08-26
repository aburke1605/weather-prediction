import numpy as np
import xarray as xr
import pandas as pd

def Open(filename, variable):
    ds = xr.open_dataset(filename)
    df = ds.to_dataframe()
    df.reset_index(drop=True, inplace=True)
    df = df[[variable, "latitude", "longitude", "month_number"]]
    df.dropna(inplace=True)