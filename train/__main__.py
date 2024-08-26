from .Utils import Open

import pandas as pd
from functools import reduce


def main():
    rainfall = Open("data/rainfall/rainfall_hadukgrid_uk_12km_mon_201001-201012.nc", "rainfall")
    sun_duration = Open("data/sun_duration/sun_hadukgrid_uk_12km_mon_201001-201012.nc", "sun")
    wind_speed = Open("data/wind_speed/sfcWind_hadukgrid_uk_12km_mon_201001-201012.nc", "sfcWind")


    data_frames = [rainfall, sun_duration, wind_speed]
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=["month_number", "latitude", "longitude"], how="outer"), data_frames)
    df_merged.dropna(inplace=True)
    print(df_merged.shape)
    print(df_merged.head())


if __name__ == "__main__":
    main()