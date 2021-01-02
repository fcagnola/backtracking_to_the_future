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
import pandas as pd

def process_citations(citations_file_path):
    data_frame = pd.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str},   # we're ensuring that the object of our DataFrame will be all strings
                                 parse_dates=['creation'])                                                # run the command to read the creation column with the knowledge of 'year', 'month' etc.
    return data_frame #['citing'].value_counts()

citations_file_path = "/Users/luisaammirati/backtracking_to_the_future/Citations/citations_sample.csv"
print(process_citations(citations_file_path))

def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'
    if len(dois) == 0:                             #    base case: if 'dois' set is empty
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'

    num = 0
    denom = 0

    # selecting only rows with year 'year'  --> we're storing in 'data_year' variable a new DataFrame = we've narrowed it down
    # we convert 'year' from string to integer, because due to 'parse_dates', the machine is able to read the object in the creation column as integer
    # the same of 'data_year = data.loc[data.creation.dt.year == int(year)]
    data_year = data.loc[data['creation'].dt.year == int(year)]

    # selecting only rows with previous two years: concatenate
    # we combine/store the two solutions ( two different DataFrames) into the same variable
    # the same if 'data.loc[data.creation.dt.year == etc.'
    data_previous_two_years = pd.concat([data.loc[data['creation'].dt.year == (int(year) - 1)], data.loc[data['creation'].dt.year == (int(year) - 2)]])

    for doi in dois:
        # selecting rows with doi == cited and adding the length of this table to num
        # num = "the number of citations all the documents in dois have received in year year" --> 'receiving a citation' refers to articles that are cited in that year (of publication of 'citing' article)
        # starting with the DataFrame obtained by line n.45,
        # we're narrowing it down again by accepting in our updated DataFrame only rows cointain , in the 'cited' column, the dois in 'dois' set
        data_year_cited = data_year.loc[data_year['cited'] == doi]
        num += len(data_year_cited)  # we count the rows of the DataFrame stored in 'data_year_cited'

        # selecting rows with doi == citing and adding the length of this table to denom
        # denom = the number of documents in dois published in the previous two years --> 'published', so we're speaking about 'citing' article
        data_previous_years_citing = data_previous_two_years.loc[data_previous_two_years['citing'] == doi]
        denom += len(data_previous_years_citing)

    print(num, denom)
    try:
        return round(num / denom, 2)
    except ZeroDivisionError:
        return "Could not compute impact factor: no DOIs pointed to objects published in \n" \
               "year-1 or year-2. Please try with another input set or year."

print(do_compute_impact_factor((process_citations(citations_file_path)),
                               {"10.1080/13548500701235732",  #2008
                                "10.3109/9780203911723-4", #2003
                                "10.1016/s0140-6736(97)11096-0" #2009
                                "10.1016/s0140-6736(97)11096-0"  #2010
                                "10.1177/2042098619854010"  #2019
                                "10.1002/14651858.cd004407.pub2" #2005
                                "10.1007/s12124-011-9160-0"}, "2005"))
print(do_compute_impact_factor(process_citations(citations_file_path),
                                {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                 '10.1097/mop.0000000000000929', # created 2020 N
                                 '10.1177/000313481107700711',   # created 2011 N
                                 '10.3414/me14-05-0004',         # created 2014 Y
                                 '10.3928/01477447-20180123-06', # created 2018 N
                                 '10.1002/ddr.21369',            # created 2016 N
                                 '10.3889/mmej.2015.50002',      # created 2015 Y
                                 '10.1016/s0140-6736(97)11096-0'}, # no creation
                                '2016'))
print(do_compute_impact_factor(process_citations(citations_file_path),
                                set(), '2016'))
print(do_compute_impact_factor(process_citations(citations_file_path),
                                 {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                 '10.1097/mop.0000000000000929', # created 2020 N
                                 '10.1177/000313481107700711',   # created 2011 N
                                 '10.3414/me14-05-0004',         # created 2014 Y
                                 '10.3928/01477447-20180123-06', # created 2018 N
                                 '10.1002/ddr.21369',            # created 2016 N
                                 '10.3889/mmej.2015.50002',      # created 2015 Y
                                 '10.1016/s0140-6736(97)11096-0'},
                                 2016))

def do_get_co_citations(data, doi1, doi2):   #doi1 and doi2 are strings identifying 2 different 'cited' article
    data_doi1_doi2 = data.loc[data['cited'].isin([doi1, doi2])]  # a Dataframe cointaining only the rows with doi1 and doi2 in 'cited' column
    # if a 'citing' document is repeat twice that means it cites both doi1 and doi2 articles (which are the only taken into account by the 'data_doi1_doi2' DataFrame
    data_less_duplicated_values = data_doi1_doi2.drop_duplicates(subset=['citing'])  #'drop_duplicate' removes duplicates on specific column(s) declared by 'subset'.

    if len(data_doi1_doi2) == len(data_less_duplicated_values): #that means that 'drop_duplicates' did not find any duplicated value, so any co-citations
        return "The doi1 and doi2 are never cited together by other documents"
    else:
        return len(data_doi1_doi2) - len(data_less_duplicated_values) #detecting how many values (duplicated) have been removed

def test_do_get_co_citations(data, doi1, doi2, expected):
    result = do_get_co_citations(data, doi1, doi2)
    if result == expected:
        return True
    else:
        return False

print(do_get_co_citations(process_citations(citations_file_path), "10.1177/000313481107700711", '10.1016/s0140-6736(97)11096-0' )) #no co-citations
print(do_get_co_citations(process_citations(citations_file_path), "10.2807/1560-7917.es.2019.24.26.1900376", '10.1016/s0140-6736(97)11096-0' )) # 1 co-citation
print(do_get_co_citations(process_citations(citations_file_path), "10.1001/archpediatrics.2009.42", '10.1016/s0140-6736(97)11096-0' )) # 1 co-citation
print(test_do_get_co_citations(process_citations(citations_file_path), "10.1177/000313481107700711", '10.1016/s0140-6736(97)11096-0', "The doi1 and doi2 are never cited together by other documents")) #True

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
