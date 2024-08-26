import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

def Open(filename:str, variable:str, rename_variable:str|None=None) -> pd.DataFrame:
    ds = xr.open_dataset(filename)
    df = ds.to_dataframe()

    # keep only variable of interest and identifiers
    df = df[[variable, "latitude", "longitude", "month_number"]]
    df.reset_index(drop=True, inplace=True)

    # remove duplicates leftover from the "bnds" columns
    df.drop_duplicates(inplace=True)

    # remove outliers
    df.dropna(inplace=True)

    # scale to between 0 and 1
    mini = min(df[variable])
    maxi = max(df[variable])
    df[variable] = (df[variable] + mini) / (mini + maxi)

    if rename_variable is not None:
        df.rename(columns={variable: rename_variable}, inplace=True)

    return df

def ReadYear(year:int) -> pd.DataFrame:
    data_frames = []
    for variable, new_variable in {
        "hurs":     "humidity",
        "tasmax":   "max_temperature",
        "tas":      "mean_temperature",
        "tasmin":   "min_temperature",
        "psl":      "pressure",
        "rainfall": "rainfall",
        "sun":      "sun_duration",
        "sfcWind":  "wind_speed",
    }.items():
        data_frames.append(Open(f"data/{new_variable}/{variable}_hadukgrid_uk_12km_mon_{year}01-{year}12.nc", variable, rename_variable=new_variable))

    data = reduce(lambda  left,right: pd.merge(left,right,on=["month_number", "latitude", "longitude"], how="outer"), data_frames)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    return data


def Plot(latitude, longitude, variable, label=None, difference=False):
    """
    x = r λ cos(φ0)
    y = r φ

    r = radius of earth
    """
    r = 6271 # km
    phi_0 = (min(latitude) + max(latitude)) / 2

    x = r * longitude * np.cos(phi_0)
    y = r * latitude

    # nbins = width / bin_width
    nbins_y = int((max(y)-min(y))/abs(y[1]-y[0]))
    # not quite the same for x, theres some curvature
    nbins_x = int((max(x)-min(x))/abs(x[1]-x[0])*2.02)

    fig, ax = plt.subplots(figsize=(6,10))
    _, _, _, im = ax.hist2d(x, y, weights=variable, bins=(nbins_x, nbins_y), cmap="coolwarm" if difference else "Blues")
    fig.colorbar(im, label=label)
    plt.show()