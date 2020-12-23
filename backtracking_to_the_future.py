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

import csv
from networkx import DiGraph


def process_citations(citations_file_path):
    g = DiGraph()  # creates directed graph

    with open(citations_file_path, mode="r") as csv_file:  # opens csv in read-mode
        reader = csv.DictReader(csv_file)

        for row in reader:    # loop through rows, each row representing a citation

            g.add_node(row['citing'], creation=row['creation'])  # creates citing node w/ attribute 'creation'

            g.add_node(row['cited'])                             # creates cited node

            g.add_edge(row['citing'], row['cited'], timespan=row['timespan'])  # creates edge w/ attribute 'timespan'

    return g  # might be better to return adjacency dict (.adj) or a tuple of (nodes, edges)


def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'
    # data is in DiGraph format

    cit_counter = 0  # this will be the dividend
    pub = set()          # this will be the divisor

    for doi in dois:
        citing = data.predecessors(doi)  # this is the network of articles citing a given DOI
        for identifier in list(citing):
            if str(data.nodes[identifier]['creation'][:4]) == year:
                cit_counter += 1  # keeps count of citations in given year

        try:   # python raises a KeyError when node doesn't have a creation date, handle it with exception
            if data.nodes[doi]['creation'][:4] == str(int(year)-1) or data.nodes[doi]['creation'][:4] == str(int(year)-2):
                pub.add(doi)          # keeps count of the DOIs published in y-1 and y-2
        except KeyError:
            pass

    return round((cit_counter / len(pub)), 2)


def do_get_co_citations(data, doi1, doi2):
    pass

def do_get_bibliographic_coupling(data, doi1, doi2):
    pass

def do_get_citation_network(data, start, end):  # F
    pass

def do_merge_graphs(data, g1, g2):              # F
    pass

def do_search_by_prefix(data, prefix, is_citing):
    pass

def do_search(data, query, field):
    pass

def do_filter_by_value(data, query, field):
    pass

# print(do_compute_impact_factor(process_citations('citations_sample.csv'),
#                                {'10.3389/fpsyg.2016.01483',
#                                 '10.1097/mop.0000000000000929',
#                                 '10.1177/000313481107700711',
#                                 '10.3414/me14-05-0004',
#                                 '10.3928/01477447-20180123-06',
#                                 '10.1002/ddr.21369',
#                                 '10.3889/mmej.2015.50002',
#                                 '10.1016/s0140-6736(97)11096-0'},
#                                '2016'))