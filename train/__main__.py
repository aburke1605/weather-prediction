from .Utils import ReadYear, Plot

import numpy as np
import pandas as pd
from functools import reduce


def main():

    data = {}
    for year in range(2010, 2010+1):#2020+1):
        # create dictionary space for this year
        data[str(year)] = {}

        # read data from this year
        all_data = ReadYear(year)

        # now split by month
        for month in range(1, 12+1):
            data[str(year)][str(month)] = all_data.query(f"month_number=={month}").drop(["month_number"], axis=1).reset_index(drop=True)
            # print(np.sum(data[str(year)][str(month)].duplicated(["latitude", "longitude"])))

        del all_data

    # simplify below for now
    june_data = data["2010"]["6"] # June
    # Plot(june_data.latitude, june_data.longitude, june_data.rainfall, "rainfall")

    # append March, April, May as separate columns
    months = [
        ("_march", data["2010"]["3"]),
        ("_april", data["2010"]["4"]),
        ("_may", data["2010"]["5"]),
    ]
    june_data = reduce(lambda left, right: pd.merge(left, right[1][["latitude","longitude","rainfall"]], how="outer", on=["latitude", "longitude"], suffixes=(None, right[0])), months, june_data)


if __name__ == "__main__":
    main()