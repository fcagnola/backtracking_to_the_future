# -*- coding: utf-8 -*-
# Copyright (c) 2020, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
#
#
# This file is just a stub of the particular module that every group should
# implement for making its project work. In fact, all these functions return None,
# which is not compliant at all with the specifications that have been provided at
# https://comp-think.github.io/2020-2021/slides/14%20-%20Project.html

import pandas
from networkx import DiGraph, from_pandas_edgelist, compose
import numpy as np
import re

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 800)


def process_citations(citations_file_path):  # years in 'YYYY' format should be 'YYYY-01-05'
    # processing through pandas' read.csv function: date parsing is necessary for easier handling of 'creation' column
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str},
                                 parse_dates=['creation'])
    return data_frame


def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'

    # Input validation
    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'

    num = 0        # numerator for the final computation
    denom = set()  # denominator for the final computation

    # Selecting all rows where 'creation' is equal to 'year'
    data_year = data.loc[data['creation'].dt.year == int(year)] # IF EMPTY SHOULD RETURN 0, SINCE NUM WILL BE 0, TO AVOID UNNECESSARY COMPUTATION
    #print('DEBUG: data_year is_______________ \n{}'.format(data_year))

    # Selecting only citations created in the previous two years:
    # a. concatenate dataframes with 'creation' == (y-1 or y-2) and reset index to be able to use integer positioning
    data_previous_two_years = pandas.concat([data.loc[data['creation'].dt.year == (int(year) - 1)], data.loc[data['creation'].dt.year == (int(year) - 2)]], ignore_index=True)

    # b. create new column for creation date of the cited articles through ancillary function
    if len(data_previous_two_years) != 0:         # prevents value and key errors if there are no results
        new_date_column = data_previous_two_years[['cited', 'creation', 'timespan']].apply(do_compute_date_column, axis=1)
        data_previous_two_years['creation_cited'] = new_date_column.values
    #print('DEBUG: data_prev_two_years is_______________ \n{}'.format(data_previous_two_years))

    # c. add DOIs in set from 'cited' column created in y-1 and y-2
    #data_previous_two_years.drop(data_previous_two_years[~data_previous_two_years['creation_cited'].isin([int(year)-1, int(year)-2])].index, inplace=True)

    for doi in dois:
        # selecting rows with doi == cited and adding the length of this table to num
        data_year_cited = data_year.loc[data_year['cited'] == doi]
        #print('DEBUG: table length will be num for {}: \n {}'.format(doi, data_year_cited))
        num += len(data_year_cited)

        # selecting rows with doi == citing and adding the length of this table to denom
        data_previous_years_citing = data_previous_two_years.loc[data_previous_two_years['citing'] == doi]
        if len(data_previous_years_citing) != 0:
            denom.add(data_previous_years_citing['citing'].iloc[0])

    print('DEBUG: num={}, denom={}'.format(num, len(denom)))
    if num == 0:
        return("Could not compute impact factor: no DOIs received citations in {}. \nPlease try with another input year or set".format(year))
    try:
        return round(num / len(denom), 2)
    except ZeroDivisionError:
        return "Could not compute impact factor: no DOIs pointed to objects published in \n" \
               "year-1 or year-2. Please try with another input set or year."


def do_get_co_citations(data, doi1, doi2):
    pass


def do_get_bibliographic_coupling(data, doi1, doi2):
    pass


def do_get_citation_network(data, start, end):  # F

    # input validation
    if int(end) < int(start):
        return "Invalid input: enter an end year greater than the start"

    timewindow = [year for year in range(start, end+1)] # list comprehension, list with all years of timewindow

    # 1. Filter data on given time window start->end (using 'creation' column)
    ls_dfs = []  # list will contain dataframes for each year in time window
    for i in timewindow:
        ls_dfs.append(data[data['creation'].dt.year == i])  # add only rows with creation year == iterator
        i += 1  # increment iterator
    d = pandas.concat(ls_dfs)

    # 2. Compute a 'creation_cited' column with dates for the cited DOIs, through ancillary function
    d['creation_cited'] = d[['cited', 'creation', 'timespan']].apply(do_compute_date_column, axis=1)
    # Remove DOIs with creation_cited != timewindow:
    d.drop(d[~d['creation_cited'].isin(timewindow)].index, inplace=True) # filter data and feed index to drop method

    # 3. Create Directed Network through networkx
    graph = from_pandas_edgelist(d, source='citing', target='cited', create_using=DiGraph)

    return graph


def do_merge_graphs(data, g1, g2):  # both input graphs will be directed

    # input validation, as per project specifications
    if type(g1) is not type(g2):
        return None

    # networkx' compose functions joins two graphs if they are of the same dtype
    return compose(g1, g2)


def do_search_by_prefix(data, prefix, is_citing):
    pass


def do_search(data, query, field):
    pass


def do_filter_by_value(data, query, field):
    pass


date_dict = dict()  # this variable will store do_compute_date_column results for future use


def do_compute_date_column(row):  # input is always pd.Series (row of a pd.DataFrame)

    global date_dict                     # allows to use global variable inside a function
    timespan = row['timespan']           # elem at index 'timespan' of the series is the timespan in 'P_Y_M_D' format
    date_column_value = row['creation']  # elem at index 'creation' is the date of creation in 'YYYY-MM-DD' format

    # if creation is only a year, add a few days to avoid weird calculations
    if str(date_column_value)[4:] == '-01-01 00:00:00':
        date_column_value = date_column_value + np.timedelta64('10', 'D')

    if row['cited'] in date_dict:        # base case: result already computed and in global dict
        return date_dict[row['cited']]

    else:                                # computation and storage for future use in the global dict

        negative = False                 # timespan is assumed to be positive
        if timespan[0] == "-":
            negative = True              # if negative, the appropriate variable will show that

        timespan = timespan.strip('PD')  # remove the 'P' at the beginning and the 'D' at the end of 'timespan'
        ls = re.split('[YM]', timespan)  # create a list in [yy, mm, dd] format for easier handling

        if not negative:                 # 1. Timespan is POSITIVE: compute by subtraction
            for idx, value in enumerate(ls):  # loop through elements in list 'ls' (could be YY, YY-MM or YY-MM-DD)
                if idx == 0:                    # first elem is always year: compute year
                    date_column_value = date_column_value - np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # second elem is always month: compute month
                    date_column_value = date_column_value - np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # third elem is always day: compute day
                    date_column_value = date_column_value - np.timedelta64(value, 'D')

        else:                            # 2. Timespan is NEGATIVE: compute by addition
            for idx, value in enumerate(ls):  # loop through elements in list 'ls' (could be YY, YY-MM or YY-MM-DD)
                if idx == 0:                    # first elem is always year: compute year
                    date_column_value = date_column_value + np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # second elem is always month: compute month
                    date_column_value = date_column_value + np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # third elem is always day: compute day
                    date_column_value = date_column_value + np.timedelta64(value, 'D')

        date_dict[row['cited']] = date_column_value.date().year   # store result for future use, to speed up processing
        return date_dict[row['cited']]
