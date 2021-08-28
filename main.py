#!/usr/bin/env python

__author__ = "Katerina Muskova"

import pandas as pd
import geopandas as gpd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt


def get_mortality(src_file_location: str = "data/mortality_per_1000.tsv") -> pd.DataFrame:
    """
    Get pabdas DataFrame filled with mortality data
    :param src_file_location: tsv data file name
    :return: created DataFrame
    """
    df = pd.read_table(src_file_location, sep='\t')

    # clean country column
    df.rename({'freq,indic_de,geo\\TIME_PERIOD': 'country'}, axis=1, inplace=True)
    df.country = df.country.str.replace('A,GDEATHRT_THSP,', "")

    # clean values
    df.replace(to_replace=r'[0-9] (e|p|b|(ep)|(bp)|(bep)|(be))$', value='', regex=True, inplace=True)
    df.replace(': ', np.nan, inplace=True)

    # column names
    year_names_orig = df.columns[1:].to_list()
    year_names_new = [y.strip() for y in year_names_orig]
    years_rename = {year_names_orig[i]: year_names_new[i] for i in range(len(year_names_new))}
    df.rename(years_rename, axis=1, inplace=True)

    # convert to appropriate data type
    years_converter = {y: float for y in year_names_new}
    df = df.astype(years_converter)
    df = df.astype({'country': "string"})

    # count extra values
    mean_cols = df.loc[:, "2017": "2019"]
    df['mean'] = mean_cols.mean(axis=1)
    df['increase'] = df['2020'] - df['mean']
    df['increase_perc'] = (df['2020'] / (df['mean'] / 100)) - 100

    return df


def get_geo_map(src_file_location='data/europe.geojson'):
    """
    Return geoDataFrame containing geo of Europe
    :return: map of Europe
    """
    geo_map = gpd.read_file(src_file_location)
    geo_map = geo_map.to_crs("EPSG:3857")

    geo_map.rename({'ISO2': 'country'}, axis=1, inplace=True)
    geo_map.loc[geo_map['country'] == 'GB', 'country'] = 'UK'
    geo_map.loc[geo_map['country'] == 'GR', 'country'] = 'EL'

    return geo_map


def add_kmeans_avg_classes(df, group_by='increase_perc', group_number=3):
    """
    Add column to dataFrame with division in groups. Value of each group is group average.
    :param df: input dataFrame
    :return: dataFrame with extra group column
    """

    # prepare input dataFrame
    km = df.sort_values(group_by, ).copy()
    km = km.loc[~df[group_by].isna()]
    km = km.loc[:, [group_by, 'country']]
    km['2d'] = km[group_by]

    # group diivision
    kmeans = KMeans(n_clusters=3).fit(km[[group_by, '2d']])
    km['class'] = kmeans.labels_
    km = km.loc[:, ['class', 'country']]

    # add division to original dataFrame
    df = df.join(km.set_index('country'), on='country', how='left')

    # extra 'best' group
    df.loc[df[group_by] < 0, 'class'] = group_number

    # count average of each group
    df = df.astype({'class': 'category'})
    level_mean = df.loc[:, ['class', group_by]].groupby('class').mean().reset_index()
    level_mean = level_mean.rename({group_by: 'mean_cls'}, axis=1)

    # add average
    df = df.join(level_mean.set_index('class'), on='class', how='left')
    df['class'] = df['mean_cls'].round(decimals=1)
    df = df.drop('mean_cls', axis=1)

    df = df.astype({'class': 'category'})
    return df


def plot_geo(df: pd.DataFrame, fig_location: str = None, show_figure: bool = False):
    """
    Plot colored map of Europe. First contains mortality per 1000 inhabitants, second
    grouped countries by percentage mortality increas.
    :param df: input daaFrame
    :param fig_location: storage of created figura
    :param show_figure: show figure
    """

    # join data with map
    geo_map = get_geo_map()
    df = df.loc[~ df['country'].isin(['EA18', 'EA19', 'EU27_2007', 'EU27_2020', 'EU28', 'FX', 'XK'])]
    df = geo_map.join(df.set_index('country'), on='country', how='right')

    # add groups
    df = add_kmeans_avg_classes(df)

    fig, axes = plt.subplots(1, 2, figsize=(11.69, 5))
    fig.suptitle("Motality increase in Europe 2020", fontsize=16)
    axes = axes.flatten()

    # plot
    plot_columns = ['increase', 'class']
    for i in range(2):
        df.plot(column=plot_columns[i], ax=axes[i], missing_kwds=dict(color="lightgrey", ), legend=True, cmap='hot')

    # modify axes
    ax_titles = ['Total increase per 1000 inhabitants', 'Average groups of percentage increase']
    for i in range(2):
        axes[i].xaxis.set_visible(False)
        axes[i].yaxis.set_visible(False)
        axes[i].set_title(ax_titles[i])

        for pos in ["top", "bottom", "right", "left"]:
            axes[i].spines[pos].set_visible(False)

    if show_figure:
        plt.show()
        plt.close()

    if fig_location is not None:
        fig.savefig(fig_location)


def add_country_names(df: pd.DataFrame):
    """
    Add country names by shortcut
    :param df: input dataFrame
    :return:
    """
    geo_map = get_geo_map()
    geo_map = geo_map.loc[:, ['country', 'NAME']]

    df = df.join(geo_map.set_index('country'), on='country', how='left')
    return df


def plot_table(df: pd.DataFrame, fig_location: str = None, show_figure: bool = False):
    """
    Plot table with European mortality sorted by percentage increase
    :param df: input dataFrame
    :param fig_location: location of created figure
    :param show_figure: whether show figure
    """

    # process data
    df = add_country_names(df)
    df.sort_values('increase_perc', inplace=True)
    df = df.loc[~df['2020'].isna()]
    df.loc[df['country'] == 'MK', 'NAME'] = 'Macedonia'

    df = pd.melt(df, id_vars=['NAME'], value_vars=['mean', '2020'], var_name='type', value_name='count')
    df.rename({'NAME': 'name'}, axis=1, inplace=True)

    # create figure
    fig, ax = plt.subplots(1, 1, figsize=(11.69, 8.27))
    fig.suptitle("Mortality per 1000 inhabitans in Europe", fontsize=16)

    # style
    sns.set_style("darkgrid")
    hls_pal = sns.color_palette("Paired", )
    hls_pal = [hls_pal[1], hls_pal[5]]
    sns.set_palette(hls_pal)

    # plot
    sns.barplot(data=df, x='name', y='count', hue='type', ax=ax)

    # modify axes
    for pos in ["top", "bottom", "right", "left"]:
        ax.spines[pos].set_visible(False)
        ax.tick_params(axis='x', labelrotation=90)

    if show_figure:
        plt.show()
        plt.close()

    if fig_location is not None:
        fig.savefig(fig_location)


def save_table(df: pd.DataFrame, table_location: str = None):
    """
    Save pandas dataFrame as csv
    :param df:
    :param table_location:
    :return:
    """
    df = add_country_names(df)
    if table_location is not None:
        df.to_csv(table_location)


def print_mean_europe(df):
    print('AVG EU:')
    print(df.loc[df['country'] == 'EU27_2020', ['mean', '2020']])


def print_sweden_increase(df):
    print('Sweden 2020:')
    print(df.loc[df['country'] == 'SE', '2020'])


def print_poland_increase(df):
    print('Poland perc increase:')
    print(df.loc[df['country'] == 'PL', ['increase_perc', '2020']])


def print_czech_increase(df):
    print('CR :')
    print(df.loc[df['country'] == 'CZ', ['increase_perc', '2020']])


def main():
    df = get_mortality()

    print_mean_europe(df)
    print_sweden_increase(df)
    print_poland_increase(df)
    print_czech_increase(df)

    plot_table(df, show_figure=False, fig_location='01_barplot.png')
    plot_geo(df, show_figure=False, fig_location='02_map.png')

    save_table(df, 'mortality_table.csv')


if __name__ == '__main__':
    main()
