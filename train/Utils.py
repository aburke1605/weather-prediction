import numpy as np
import xarray as xr
import pandas as pd

def Open(filename, variable) -> pd.DataFrame:
    ds = xr.open_dataset(filename)
    df = ds.to_dataframe()
    df.reset_index(drop=True, inplace=True)

    # keep only variable of interest and identifiers
    df = df[[variable, "latitude", "longitude", "month_number"]]

    # remove outliers
    df.dropna(inplace=True)

    # scale to between 0 and 1
    mini = min(df[variable])
    maxi = max(df[variable])
    df[variable] = (df[variable] + mini) / (mini + maxi)

    return df