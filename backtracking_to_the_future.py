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

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 800)

def process_citations(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str},
                                 parse_dates=['creation'])
    return data_frame

dataframe = process_citations(r"./citations_sample.csv")
print(dataframe)

def do_compute_impact_factor(data,dois,year):
    pass

def do_get_co_citations(data, doi1, doi2):
    pass

#It returns an integer defining how many times the two input documents cite both the same document.
def do_get_bibliographic_coupling(data, doi1,doi2):
    if doi1 == doi2:
        return "Please change one of the DOIs inserted."
    data_doi1_doi2 = data[['citing', 'cited']].loc[data['citing'].isin([doi1,doi2])]
    print(data_doi1_doi2)
    less_duplicate = data_doi1_doi2.drop_duplicates(subset=['cited'])
    if len(data_doi1_doi2) == len(less_duplicate):
        return "The doi1 and the doi2 don't cite both the same document."
    else:
        return len(data_doi1_doi2) - len(less_duplicate)

data = process_citations(r"./citations_sample.csv")
#doi1 = '10.1007/978-3-319-93293-4_2'
#doi2 = '10.3390/vaccines8040600'
#OUTPUT : The doi1 and the doi2 don't cite both the same document.

doi1 = '10.1007/978-3-319-93293-4_2'
doi2 = '10.1007/978-3-319-93224-8_30'
#OUTPUT: 1
print(do_get_bibliographic_coupling(data,doi1,doi2))

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
