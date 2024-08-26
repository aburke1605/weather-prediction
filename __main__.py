from .Utils import Open


def main():
    Open("./data/wind_speed/sfcWind_hadukgrid_uk_12km_mon_201001-201012.nc", "sfcWind")


if __file__ == "__main__":
    main()