from .Utils import ReadYear, Plot

import numpy as np
import pandas as pd


def main():

    data = {}
    for year in range(2010, 2010+1):#2020+1):
        # create dictionary space for this year
        data[str(year)] = {}

        # read data from this year
        all_data = ReadYear(year)

        # now split by month
        for month in range(1, 12+1):
            data[str(year)][str(month)] = all_data.query(f"month_number=={month}").drop(["month_number"], axis=1)
            # print(np.sum(data[str(year)][str(month)].duplicated(["latitude", "longitude"])))

        del all_data

if __name__ == "__main__":
    main()