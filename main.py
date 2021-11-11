import os
import pandas as pd
from glob import glob
import numpy as np
from datetime import timedelta as td

columns = ['Команди на розвантаження, МВт*год',
           'Команди на завантаження, МВт*год',
           'Обсяг відбору (споживання), КВт*год',
           'Обсяг відпуску (генерації), МВт*год']
columns_order = ['День', 'Розрахунковий період'] + columns


def create_df(name):
    df = pd.read_csv(name, sep=';', index_col=0, usecols=[0, 3, 4, 5, 6], skiprows=1)
    df.replace(np.nan, 0, regex=True, inplace=True)
    df.replace({'ff': 0, 'f': '', ',': '', np.nan: 0, '-': ''}, regex=True, inplace=True)
    df = df.astype(float)
    df.index = pd.to_datetime(df.index.str[:-8], format='%d.%m.%Y %H:%M')
    df.columns = columns
    df = df / 1000
    df[columns[0]] *= -1
    df[columns[2]] *= -1
    return df


def main():
    list_df = []
    cwd = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(cwd, 'input', '*.csv')
    dir_list = glob(target)
    for item in dir_list:
        list_df.append(create_df(item))
    df = pd.concat(list_df)
    df = df.groupby(pd.Grouper(freq='H')).sum()
    df['День'] = df.index.date
    df['Розрахунковий період'] = df.index.time.astype(str)
    df['Розрахунковий період'] += ' - '
    df['Розрахунковий період'] += (df.index + td(hours=1)).time.astype(str)
    df = df[columns_order]
    print(df.head().to_string())
    df.to_excel('output_result.xlsx', index=False)


if __name__ == '__main__':
    main()
