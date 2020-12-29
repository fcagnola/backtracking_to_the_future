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
# implement for making its project work. In fact, all these functions returns None,
# which is not compliant at all with the specifications that have been provided at
# https://comp-think.github.io/2020-2021/slides/14%20-%20Project.html

import pandas
from networkx import DiGraph
import numpy as np

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 800)


def process_citations(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str},
                                 parse_dates=['creation'])
    return data_frame


def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'
    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'

    num = 0
    denom = 0

    # selecting only rows with year 'year'
    data_year = data.loc[data['creation'].dt.year == int(year)]

    # selecting only rows with previous two years
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
    i = int(start)  # iterator, set as ==start, then 1 is added each iter until 'end' is reached
    ls_dfs = []  # list will contain dataframes for years in time window
    while i != (int(end) + 1):
        ls_dfs.append(data[data['creation'].dt.year == i])  # returns 436 instead of 442 rows
        i += 1
    dataset = pandas.concat(ls_dfs)  # the dataframe to convert to graph
    # ALL DOIs in the second column MUST also be in the first, otherwise remove that row.

    # create network (use developed function)
    graph = DiGraph()


print(do_get_citation_network(
    process_citations('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'), 2018,
    2020))


def do_merge_graphs(data, g1, g2):  # F
    pass


def do_search_by_prefix(data, prefix, is_citing):
    pass


def do_search(data, query, field):
    pass


def do_filter_by_value(data, query, field):
    pass
