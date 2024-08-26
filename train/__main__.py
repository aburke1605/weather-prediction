from .Utils import ReadYear, Plot

import numpy as np
import pandas as pd
from functools import reduce

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

import gc

def main():

    data = {}
    for year in range(2010, 2010+1):#2020+1):

        # read data from this year
        year_data = ReadYear(year)

        # want to end up having "rainfall" and other columns for each month
        # i.e. rainfall_jan, rainfall_feb, wind_speed_jun etc

        # melt the 'measurement' columns into one very long data frame which also has 'value's
        melted_data = year_data.melt(id_vars=['latitude', 'longitude', 'month_number'], var_name='measurement', value_name='value')

        # now 'pivot' or rotate these columns so we get back to having the 'measurement's only in the column headers
        pivoted_data = melted_data.pivot_table(index=['latitude', 'longitude'], columns=['measurement', 'month_number'], values='value')

        # flatten the now multi-level column index
        pivoted_data.columns = [f"{measurement}_{month}" for measurement, month in pivoted_data.columns]
        # reset index
        reformatted_year_data = pivoted_data.reset_index()

        # make sure the final data frame is a factor of 12 shorter
        # since we have moved the 12 individual months into their own columns
        assert year_data.shape[0] == reformatted_year_data.shape[0] * 12

        # the number of 'measurement' variables should be equal to:
        #         tot_n_cols     (-latitude -longitude    -month_number) ==            total_n_cols         (-latitude -longitude)   per  month
        assert year_data.shape[1]           -2                 -1        == (reformatted_year_data.shape[1]           -2         )    /    12

        # finally, make sure there are no duplicated latitude and longitude coordinates
        assert np.sum(reformatted_year_data.duplicated(["latitude", "longitude"])) == 0
        data[str(year)] = reformatted_year_data

        gc.collect()



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