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
    g = DiGraph()  # for citations a directed graph would be the best choice

    with open(citations_file_path, mode="r") as csv_file:  # opening csv in read-mode
        reader = csv.DictReader(csv_file)

        for row in reader:    # loop through rows, each row representing a citation
            g.add_node(row['citing'], creation=row['creation'])  # create the citing node, with attribute 'creation'
            g.add_node(row['cited'])                             # create cited node
            g.add_edge(row['citing'], row['cited'], timespan=row['timespan'])  # create edge with timespan as attribute

    return g  # i wonder if it would be better to return the adj dictionary or a tuple of (nodes, edges)


def do_compute_impact_factor(data, dois, year):  # dois is a set, year is 4 digit string 'YYYY'

    # data is in graph format, for this function only node data is required, so store that in a variable
    nodes = data.nodes(data=True)

    cit_counter = 0  # this will be the dividend
    pub = 0          # this will be the divisor

    for node in nodes:  # loop through nodes and dois given as parameter
        for doi in dois:

            # if the node is a citing one, and creation-year is == YEAR and the citing node is in set of dois
            if node[1] != {} and node[1]['creation'][:4] == year and node[0] == doi: # for efficiency testing, we should try inverting conditions
                cit_counter += 1  # add one to the dividend

            # if node is citing and year is year-1 or year-2 add 1 to the divisor
            if len(node[1]) != 0:
                if node[1]['creation'][:4] == str(int(year)-1) or node[1]['creation'][:4] == str(int(year)-2):
                    pub += 1

    return round((cit_counter / pub), 2)  # this tries to solve float errors or weird divisions


def do_get_co_citations(data, doi1, doi2):
    pass

def do_get_bibliographic_coupling(data, doi1, doi2):
    pass

def do_get_citation_network(data, start, end):
    pass

def do_merge_graphs(data, g1, g2):
    pass

def do_search_by_prefix(data, prefix, is_citing):
    pass

def do_search(data, query, field):
    pass

def do_filter_by_value(data, query, field):
    pass
print(do_compute_impact_factor(process_citations('citations_sample.csv'),
                               {'10.1007/978-3-319-94694-8_26','10.3390/vaccines7040201', '10.3390/vaccines8040600', '10.3414/me14-05-0004'},
                               '2019'))