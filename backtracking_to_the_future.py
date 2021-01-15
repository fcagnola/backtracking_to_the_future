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

def process_citations(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str}, parse_dates=['creation'])
    return data_frame

cit_pandas_dates = process_citations('citations_sample.csv')

def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'
    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'

    num = 0
    denom = 0

    # selecting only rows with year 'year'
    data_year = data.loc[data['creation'].dt.year == int(year)]

    # selecting only rows with previous two years: concatenate
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

def do_get_citation_network(data, start, end):
    pass

def do_merge_graphs(data, g1, g2):
    pass

def do_search_by_prefix(data, prefix, is_citing):
    #defining the query to do on the fields using Regex
    query = prefix+'/.*'

    #deciding on which field to do the query
    if is_citing:
        field = 'citing'
    else:
        field = 'cited'

    filtered_data = data[data[field].str.count(query)>0]
    if len(filtered_data) == 0:
        return "The input prefix cannot be found. Please insert a new one."
    else:
        #returning a subcollection of the data where the query on the right field is true
        return filtered_data

print(do_search_by_prefix(cit_pandas_dates, '10.3390', True))
print(do_search_by_prefix(cit_pandas_dates, '10.1016', False))

#the function is working, but can't be used with 'creation' as Date format, I have to find a way to deal with it
def do_search(data, query, field):

    #preliminary verifications on the data provided
    if type(query) is not str or query == '':
        return 'Please provide a valid string as a query'
    if field not in data.columns:
        return 'Please provide a valid field for the data'

    #base case: if there are no operators expcept 'not'
    if not re.search(r'(\sand\s|\sor\s)', query):

        #the search will be case insensitive
        result = '(?i)'

        # transforms the query in correct regex and escapes ambiguous characters
        for letter in query:
            if letter == '*':
                result += '.*'
            elif letter == '.':
                result += '\.'
            elif letter == '(':
                result += '\('
            elif letter == ')':
                result += '\)'
            else:
                result += letter

        #if the query contains 'not'
        if re.findall(r'\bnot\s', query) != []:

            #removes the word from the query
            result = re.sub(r'\bnot\s', r'', result)
            print("There's a 'not'")
            print(result)

            if field == "creation":
                return data[data[field].dt.strftime("%Y-%m-%d").str.count(result)==0]
            else:
                #selects only the rows where the statement is not true on the column 'field'
                return data[data[field].str.count(result)==0]
        elif field == "creation":
            print(result)
            return data[data[field].dt.strftime("%Y-%m-%d").str.count(result)>0]

        else:
            print(result)
            # else selects only the rows where the query returns true on the column 'field'
            return data[data[field].str.count(result)>0]

    #recursive cases: when there are some 'and' or 'or'
    else:

        # we first deal with or because in python 'and' has the priority: must be dealt with last
        # for example: True or True and False = True or (True and False) = True or False = True
        # an example for our data: x or y and z will be dealt as [x, y and z] first, to make sure that 'y and z' will be evaluated.
        # otherwise, it would be (x or y) and z and we don't want that
        if re.search(r'(\sor\s)', query):

            #splits the query in two and removes the 'or'
            splitted = query.split(' or ')
            print("there's an 'or':", splitted)

            #This time the two recursions are done separately and joined in the return statement
            left = do_search(data, splitted[0], field)
            #The .join function is to treat a query with multiple 'or'
            right = do_search(data, ' or ' .join(splitted[1:]), field)

            #how = 'outer' uses the union of keys from both Dataframes. Attention: the keys are not mainained
            return left.merge(right, how='outer')
            # if the first one is an 'and'

        if re.search(r'(\sand\s)', query):

            # splits the query in two and removes 'and'
            splitted = query.split(' and ')
            print("there's an 'and':",splitted)
            # in this line there are two recursions: the data provided to the second part of the query
            # is the one returned by the call of this function on the first part.
            # The .join function allows the query to have multiple 'and' inside and treats them one after the other.
            return do_search(do_search(data, splitted[0], field), ' and '.join(splitted[1:]), field)

print(do_search(citations_pandas, 2, 'citing'))
print(do_search(citations_pandas, 'hello', 'cit'))
print(do_search(citations_pandas, 'ArcHdischIld', 'citing'))
print("Doing the search for '-01 and not 2008' :\n", do_search(citations_pandas, '-01 and not 2008', 'creation'))
print("Doing the search for '2007 or not 2008 and -01 or -02' :\n", do_search(citations_pandas, '2007 or not 2008 and -01 or -02', 'creation'))
print("Doing the search for '10.1057*biosoc' :\n", do_search(citations_pandas, '10.1057*biosoc', 'citing'))
print("Doing the search for '01461672 and 115' :\n", do_search(citations_pandas, '01461672 and 115', 'cited'))

def do_filter_by_value(data, query, field):
    pass
