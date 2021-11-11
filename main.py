import os
import pandas as pd
from glob import glob
import numpy as np
import re


def create_df(name):
    df = pd.read_csv(name, sep=';', index_col=0)
    print(df)
    return df


def main():
    list_csv = []
    cwd = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(cwd, "input", '*HPP.csv')
    dir_list = glob(target)
    for item in dir_list:
        name_df = create_df(item)
        list_csv.append(name_df)


if __name__ == '__main__':
    main()