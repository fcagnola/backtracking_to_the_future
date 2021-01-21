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


def process_citations(citations_file_path):
    # processing through pandas' read.csv function: date parsing is necessary for easier handling of 'creation' column
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str},
                                 parse_dates=['creation'])
    return data_frame


def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'

    # Input validation: alternatively use isinstance(value, type)
    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) is int:
        return 'Please provide a year in string format: "YYYY"'

    # Filter dataframe: all rows that have one of the DOIs in the 'citing' or 'cited' column
    dois_in_cited = data[data['cited'].isin(dois)].reset_index(drop=True)
    dois_in_citing = data[data['citing'].isin(dois)].reset_index(drop=True)

    # Create new column for creation date of the cited articles through ancillary function
    dois_in_cited['creation_cited'] = dois_in_cited[['cited', 'creation', 'timespan']].apply(do_compute_date_column, axis=1)

    # Select all rows of DOIs cited in year 'year'
    table_num = dois_in_cited.loc[dois_in_cited['creation'].dt.year == int(year)]
    num = len(table_num.citing.unique())
    if num == 0:    # avoid unnecessary computations if numerator is equal to 0: return error right away
        return ("Could not compute impact factor: no DOIs received citations in {}. \nPlease try with another input year or set".format(year))

    # Filtering for DOIs created in the previous two years:
    #   concatenate dataframes with (y-1 or y-2) in 'creation' or 'creation_cited' column and reset index
    y_1_2_citing = dois_in_citing.loc[(dois_in_citing['creation'].dt.year == (int(year) - 1)) | (dois_in_citing['creation'].dt.year == (int(year) - 2))]
    y_1_2_cited = dois_in_cited.loc[(dois_in_cited['creation_cited'] == (int(year) - 1)) | (dois_in_cited['creation_cited'] == (int(year) - 2))]
    #   create sets of unique values for the two columns 'cited' and 'citing', and unite these sets (no duplicates)
    denom1 = set(y_1_2_cited['cited'].unique())
    denom2 = set(y_1_2_citing['citing'].unique())
    denom = len(denom1.union(denom2))
    if denom == 0:  # avoid ZeroDivisionError and handle case
        return "Could not compute impact factor: no DOIs pointed to objects published in \nyear-1 or year-2. Please try with another input set or year."

    # Return the result as a rounded numer to the 2nd decimal point
    return round(num / denom, 2)


def do_get_co_citations(data, doi1, doi2):
    pass


def do_get_bibliographic_coupling(data, doi1, doi2):
    pass


def do_get_citation_network(data, start, end):

    # Input validation
    if int(end) < int(start):
        return "Invalid input: enter an end year greater than the start"

    # List all years in the timewindow start->end
    timewindow = [year for year in range(int(start), int(end)+1)]

    # Filter data using 'creation' column:
    ls_dfs = []  # list will contain one dataframe for each year in time window
    for i in timewindow:
        ls_dfs.append(data[data['creation'].dt.year == i])

    # Concatenate all dataframes into a single df for all years in time timewindow: if empty return Error
    d = pandas.concat(ls_dfs)
    if len(d) == 0:
        return "Error, could not compute graph, no documents were created in the specified timewindow \nPlease try with another start-end combination"

    # Compute a 'creation_cited' column with dates for the cited DOIs, through ancillary function
    d['creation_cited'] = d[['cited', 'creation', 'timespan']].apply(do_compute_date_column, axis=1)
    # Remove DOIs with creation_cited != timewindow:
    #   filter data and feed the filtered index to .drop method, inplace allows to do it directly on d
    d.drop(d[~d['creation_cited'].isin(timewindow)].index, inplace=True)

    # Create Directed Network through networkx
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
                if idx == 0:                    # first elem is year: compute year
                    date_column_value = date_column_value - np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # second elem is month: compute month
                    date_column_value = date_column_value - np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # third elem is day: compute day
                    date_column_value = date_column_value - np.timedelta64(value, 'D')

        else:                            # 2. Timespan is NEGATIVE: compute by addition
            for idx, value in enumerate(ls):  # loop through elements in list 'ls' (could be YY, YY-MM or YY-MM-DD)
                if idx == 0:                    # first elem is year: compute year
                    date_column_value = date_column_value + np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # second elem is month: compute month
                    date_column_value = date_column_value + np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # third elem is day: compute day
                    date_column_value = date_column_value + np.timedelta64(value, 'D')

        date_dict[row['cited']] = date_column_value.date().year   # store result for future use, to speed up processing
        return date_dict[row['cited']]
