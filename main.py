import os
import pandas as pd
from glob import glob
import numpy as np
from functools import reduce


def create_df(name):
    df = pd.read_csv(name, sep=';', index_col=0)
    df.replace(np.nan, 0, regex=True, inplace=True)
    df = df.drop(df.columns[6], axis=1)
    df = df.iloc[1:]
    columns = df.columns
    for col in columns:
        df.loc[df[col] == "ff", col] = np.nan
        df[col] = df[col] \
            .replace('f', '', regex=True)
        df[col] = df[col] \
            .replace('-', '', regex=True)
        df[col] = df[col] \
            .replace(',', '', regex=True)
    for col in columns:
        df = df.astype(float)
        df[col] = df[col].div(1000).round(decimals=3)
        df[col].apply(lambda x: f'{x:.0f}')
    df.fillna(0, inplace=True)
    return df


def main():
    list_df = []
    cwd = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(cwd, "input", '*HPP.csv')
    dir_list = glob(target)
    for item in dir_list:
        name_df = create_df(item)
        list_df.append(name_df)
    df_result = reduce(lambda a, b: a.add(b, fill_value=0), list_df)
    # df_result = df_result.astype(str)

    # for col in df_result.columns:
    #     df_result[col] = df_result[col] \
    #         .replace('\\.', ',', regex=True)  # required format

    df_result.to_csv('output_result.csv', sep=';')
    print(df_result)


if __name__ == '__main__':
    main()
