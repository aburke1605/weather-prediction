from .Utils import Open

import pandas as pd
from functools import reduce


def main():

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
        data_frames.append(Open(f"data/{new_variable}/{variable}_hadukgrid_uk_12km_mon_201001-201012.nc", variable, rename_variable=new_variable))

    data = reduce(lambda  left,right: pd.merge(left,right,on=["month_number", "latitude", "longitude"], how="outer"), data_frames)
    data.dropna(inplace=True)
    print(data.shape)
    print(data.head())

if __name__ == "__main__":
    main()