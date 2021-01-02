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
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str}, parse_dates=['creation'])
    return data_frame


def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'

    # input validation
    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'

    num = 0         # numerator for the final computation
    denom = 0       # denominator for the final computation

    # selecting only citations by documents published in year 'year'
    data_year = data.loc[data['creation'].dt.year == int(year)]

    # selecting only citations with previous two years: concatenate
    data_previous_two_years = pandas.concat([data.loc[data['creation'].dt.year == (int(year) - 1)], data.loc[data['creation'].dt.year == (int(year) - 2)]])

    for doi in dois:
        # selecting rows with doi == cited and adding the length of this table to num
        data_year_cited = data_year.loc[data_year['cited'] == doi]
        num += len(data_year_cited)

        # selecting rows with doi == citing and adding the length of this table to denom
        data_previous_years_citing = data_previous_two_years.loc[data_previous_two_years['citing'] == doi]
        denom += len(data_previous_years_citing)

    try:
        return round(num / denom, 2)
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

    # filter data on given time window start->end
    i = int(start)      # iterator, set as ==start, then 1 is added each iter until 'end' is reached
    ls_dfs = []         # list will contain dataframes for each year in time window
    while i != (int(end) + 1):
        ls_dfs.append(data[data['creation'].dt.year == i])  # add only rows with creation year == iterator
        i += 1                                              # increment iterator

    # concatenate dataframes, create dataframe for whole timewindow (start>end)
    d = pandas.concat(ls_dfs)
    # compute a 'creation_cited' column with dates for the cited DOIs, through an ancillary function
    d['creation_cited'] = d[['creation', 'timespan']].apply(do_compute_date_column, axis=1)
    # NEED TO REMOVE DOIs WHICH HAVE CREATION CITED VALUE != TIMEWINDOW START-END

    # create actual Directed Network through networkx
    graph = from_pandas_edgelist(d, source='citing', target='cited', create_using=DiGraph)

    return graph


def do_merge_graphs(data, g1, g2):  # F
    # available functions are 'compose' and 'update'
    g = compose(g1, g2)
    return g


def do_search_by_prefix(data, prefix, is_citing):
    pass


def do_search(data, query, field):
    pass


def do_filter_by_value(data, query, field):
    pass


def do_compute_date_column(row):  # this function takes a pd.Series as input (row of a pd.DataFrame)

    timespan = row['timespan']    # the elem at index 'timespan' is the timespan in 'P_Y_M_D' format
    creation = row['creation']    # the elem at index 'creation' is the date of creation in 'YYYY-MM-DD' format

    negative = False              # timespan could be negative, in that case the computation should be reversed
    if timespan[0] == "-":
        negative = True

    timespan = timespan.strip('PD')     # i remove the 'P' at the beginning and the 'D' at the end of the timespan
    ls = re.split('[YM]', timespan)     # then a list is created in [yy, mm, dd] format

    date_column_value = creation        # this will be the return value: computed creation time for cited DOI
    if not negative:
        for idx, value in enumerate(ls):    # loop through elements in the list (there could be YY, YY-MM or YY-MM-DD)
            if idx == 0:                    # first elem will always be year: compute year by subtraction
                date_column_value = date_column_value - np.timedelta64(value, 'Y')
            elif idx == 1 and value != '':  # second elem will always be month: compute month by subtraction
                date_column_value = date_column_value - np.timedelta64(value, 'M')
            elif idx == 2 and value != '':  # third elem will always be day: compute day by subtraction
                date_column_value = date_column_value - np.timedelta64(value, 'D')
    else:
        for idx, value in enumerate(ls):    # loop through elements in the list (there could only be YY or YY-MM)!
            if idx == 0:                    # first elem will always be year: compute year by subtraction
                date_column_value = date_column_value + np.timedelta64(value, 'Y')
            elif idx == 1 and value != '':  # second elem will always be month: compute month by subtraction
                date_column_value = date_column_value + np.timedelta64(value, 'M')
            elif idx == 2 and value != '':  # third elem will always be day: compute day by subtraction
                date_column_value = date_column_value + np.timedelta64(value, 'D')

    return date_column_value.date() #.year only returns the year, could be wise since it is not a perfect computation


g = do_get_citation_network(
    process_citations('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'), 2018,
    2020)
h = do_get_citation_network(process_citations('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'), 2011,
    2018)
u = do_merge_graphs(process_citations('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'),g,h)

print(len(u.edges), len(h.edges)+len(g.edges))