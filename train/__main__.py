from .Utils import Open

import pandas as pd
from functools import reduce


def main():

    data_frames = []
    for variable, new_variable in {
        "rainfall": "rainfall",
        "sun": "sun_duration",
        "sfcWind": "wind_speed",
    }.items():
        data_frames.append(Open(f"data/{new_variable}/{variable}_hadukgrid_uk_12km_mon_201001-201012.nc", variable, rename_variable=new_variable))

    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=["month_number", "latitude", "longitude"], how="outer"), data_frames)
    df_merged.dropna(inplace=True)


if __name__ == "__main__":
    main()