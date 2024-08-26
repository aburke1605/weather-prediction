import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

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

    fig, ax = plt.subplots(figsize=(6,10))
    _, _, _, im = ax.hist2d(x, y, weights=variable, bins=150, cmap="coolwarm" if difference else "Blues")
    fig.colorbar(im, label=label)
    plt.show()