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


def process_citations(citations_file_path):
    #return list that will contain every line as a dictionary
    matrix = list()

    #opens file
    with open(citations_file_path, mode='r', encoding='utf-8') as file:

        #turns every line into a dictionary
        csvFile = csv.DictReader(file)

        #append every line as dictionary to the list of lines
        for line in csvFile:
            matrix.append(line)

    return matrix

def do_compute_impact_factor(data, dois, year):
    # variables for counting the number of citations and the number of articles in the previous years
    num_citations = 0
    num_published_prec_years = 0

    # turning the year into an integer to substract easily
    year_int = int(year)

    # iterating over all the data and all the dois
    for doi in dois:
        for line in data:

            # checks if the doi has been cited in year 'year'
            if doi == line['cited'] and year == line['creation'][:4]:
                num_citations += 1

            # checks if the doi is a citing article and has been published in the previous two years
            if doi == line['citing'] and (
                    line['creation'][:4] == str(year_int - 1) or line['creation'][:4] == str(year_int - 2)):
                num_published_prec_years += 1

    # return IF
    return num_citations / num_published_prec_years

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
