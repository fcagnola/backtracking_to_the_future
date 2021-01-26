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
from networkx import DiGraph, from_pandas_edgelist, compose
import numpy as np
import re


def process_citations(citations_file_path):
    # processing through pandas' read.csv function: date parsing is necessary for easier handling of 'creation' column
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str}, parse_dates=['creation'])
    return data_frame


def do_compute_impact_factor(data, dois, year):

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


def do_get_co_citations(data, doi1, doi2):   #doi1 and doi2 are strings identifying 2 different 'cited' article
    # Input validation
    if doi1 == doi2:
        return 'Please change one of the DOIs inserted'
    # DataFrame containing only the rows with doi1 and doi2 in 'cited' column
    data_doi1_doi2 = data[["citing", "cited"]].loc[data['cited'].isin([doi1, doi2])]  
    # if a 'citing' document is repeat twice that means it cites both doi1 and doi2 articles: select all duplicate rows based on one column
    duplicate_rows = data_doi1_doi2[data_doi1_doi2.duplicated(subset=['citing'])]  
    if len(duplicate_rows) == 0:
        return "The doi1 and doi2 are never cited together by other documents"
    else:
        return len(duplicate_rows)    

def do_get_bibliographic_coupling(data, doi1,doi2):
    #The function returns an integer defining how many times the two input DOIs cite both the same document.

    if doi1 == doi2:
        return "Please change one of the DOIs inserted."

    #It returns a dataframe containing the 'citing' and 'cited' columns 
    #of the two different DOIs stored in the variable doi1 and doi2.
    data_doi1_doi2 = data[['citing', 'cited']].loc[data['citing'].isin([doi1,doi2])]

    #This line removes one of the 'cited' DOIs, if repeated twice.
    less_duplicate = data_doi1_doi2.drop_duplicates(subset=['cited'])

    #Case of dataframe without 'cited' duplicates: the two DOIs cite different documents.
    if len(data_doi1_doi2) == len(less_duplicate):
        return "The doi1 and the doi2 don't cite both the same document."
    #Case with 'cited' duplicates: it is returned how many times the two input DOIs cite both the same document.
    else:
        return len(data_doi1_doi2) - len(less_duplicate)

def do_get_citation_network(data, start, end):

    # Input validation
    if int(end) < int(start):
        return "Invalid input: enter an end year greater than the start"

    # 1. List all years in the timewindow start->end
    timewindow = [year for year in range(int(start), int(end)+1)]

    # 2. Filter data using 'creation' column:
    ls_dfs = []  # list will contain one dataframe for each year in time window
    for i in timewindow:
        ls_dfs.append(data[data['creation'].dt.year == i])

    # 3. Concatenate all dataframes into a single df for all years in time timewindow: if empty return Error
    d = pandas.concat(ls_dfs)
    if len(d) == 0:
        return "Error, could not compute graph, no documents were created in the specified timewindow \nPlease try with another start-end combination"

    # 4. Compute a 'creation_cited' column with dates for the cited DOIs, through ancillary function
    d['creation_cited'] = d[['cited', 'creation', 'timespan']].apply(do_compute_date_column, axis=1)
    # Remove DOIs with creation_cited != timewindow:
    #   filter data and feed the filtered index to .drop method, inplace allows to do it directly on d
    d.drop(d[~d['creation_cited'].isin(timewindow)].index, inplace=True)

    # Create Directed Network through networkx
    graph = from_pandas_edgelist(d, source='citing', target='cited', create_using=DiGraph)

    return graph


def do_merge_graphs(data, g1, g2):

    # input validation, as per project specifications
    if type(g1) is not type(g2):
        return None

    # networkx' compose functions joins two graphs if they are of the same dtype
    return compose(g1, g2)


def do_search_by_prefix(data, prefix, is_citing):

    #defining the query to do using regex: the prefix is in input, only  '/' and 'any character' are added
    query = prefix+'/.*'

    #deciding on which field to do the query
    if is_citing:
        field = 'citing'
    else:
        field = 'cited'

    #selection of the dataframe in input where the query matches on the field requested
        #.str.count(query) searches for the number of matches on a Series for a query with regex
    filtered_data = data[data[field].str.count(query) > 0]

    #if the dataframe is empty: informs the user that the prefix cannot be found
    if len(filtered_data) == 0:
        return "The input prefix cannot be found. Please insert a new one."

    else:
        #returning the subcollection of the data as requested in input
        return filtered_data

def do_search(data, query, field):

    #preliminary verifications on the input values provided
    if type(query) is not str or query == '':
        return 'Please provide a valid string as a query'
    if field not in data.columns:
        return 'Please provide a valid field for the data'
    if re.search(r'\snot\s', query, re.I):
        if not re.search(r'\sand\snot\s|\sor\snot\s', query, re.I):
            return 'Please provide an operator "and" or "or" before the "not"'

    #base case: if there are no operators expcept 'not'
    if not re.search(r'(\sand\s|\sor\s)', query):

        #the search will be case insensitive
        result = '(?i)'

        # transforms the query in correct regex and escapes ambiguous characters
        for letter in query:
            if letter == '*':
                result += '.*'
            elif letter in '.^${}+-?()[]\|':
                result += '\\'+letter
            else:
                result += letter

        # if the query contains 'not'
        if re.search(r'\bnot\s', query):

            #removes the word from the query, because the operation will be done in the return statement
            result = re.sub(r'\bnot\s', r'', result)

            if field == "creation":

                # returns the date from DateTime to the original "yyyy-mm-dd" format
                return data[data[field].dt.strftime("%Y-%m-%d").str.count(result)==0]
            else:

                # selects only the rows where the statement is not found in the column 'field'
                return data[data[field].str.count(result)==0]

        elif field == "creation":

            # returns the date from DateTime to the original "yyyy-mm-dd" format
            return data[data[field].dt.strftime("%Y-%m-%d").str.count(result)>0]

        else:

            # else selects only the rows where the query returns true on the column 'field'
            return data[data[field].str.count(result)>0]

    #recursive cases: when there are some 'and' or 'or'
    else:

        # we first deal with 'or' because in python 'and' has the priority: must be dealt with last
        if re.search(r'(\sor\s)', query):

            #splits the query in two and removes the 'or'
            splitted = query.split(' or ')

            # the two recursions are done separately and joined in the return statement
            left = do_search(data, splitted[0], field)
            
            # The .join function is to treat a query with multiple 'or'. 
            #   Without it, a statement like '2007 or 2003 or 2005' would be dealt only as '2007 or 2003'
            right = do_search(data, ' or ' .join(splitted[1:]), field)

            #how = 'outer' uses the union of keys from both Dataframes. Warning: the keys are not maintained
            return left.merge(right, how='outer')
            # if the first one is an 'and'
        
        # if there is an 'and'
        if re.search(r'(\sand\s)', query):

            # splits the query in two and removes 'and'
            splitted = query.split(' and ')
            
            # in this line there are two recursions: the data provided to the second part of the query
            # is the one returned by the call of this function on the first part.
            # The .join function allows the query to have multiple 'and' inside and treats them one after the other.
            return do_search(do_search(data, splitted[0], field), ' and '.join(splitted[1:]), field)

def do_filter_by_value(data, query, field):  
    
    #Input validation
    if type(query) is not str or query == '':
        return 'Please provide a valid string as a query'
    if field not in data.columns:
        return 'Please provide a valid field for the data'
    if re.search(r'\snot\s', query, re.I):
        if not re.search(r'\sand\snot\s|\sor\snot\s', query, re.I):
            return 'Please provide an operator "and" or "or" before the "not"'
   
    #case insensitive
    query = query.lower()
   
    # we convert the "creation" column object into string dtype, consequent to the initial conversion in process_citation function
    if field == 'creation' and data[field].dtype != object:
        data['creation'] = data['creation'].dt.strftime("%Y-%m-%d")
    
    # base case: if there is no 'and' or 'or'.
    if not re.search(r'(\sand\s|\sor\s)', query):
        if " " not in query :                                # case: only <token> without operators
            if field == "timespan":
                query = query.upper()            
            return data[data[field] == query]
        
        elif re.search(r'(\bnot\s)', query):                 # case: <not> <operator> <token> ; Ex.["not", "==", "2001"]
            
            if field == "timespan":
                query = query.upper()            
            
            qy = query.split(' ')                            
            if qy[1] == "==":                                
                return data[~data[field] == qy[2]]
            if qy[1] == "!=":
                return data[~data[field] != qy[2]]
            if qy[1] == ">":
                return data[~data[field] > qy[2]]
            if qy[1] == ">=":
                return data[~data[field] >= qy[2]]
            if qy[1] == "<=":
                return data[~data[field] <= qy[2]]
            if qy[1] == "<":
                return data[~data[field] < qy[2]]
            else:
                return data[data[field] != qy[1]]
        else:
            
            if field == "timespan":
                query = query.upper()  
            
            qy = query.split(' ')                            # case: <operator> <token>; Ex. ["==", "2001"]
            if qy[0] == "==":  
                return data[data[field] == qy[1]]
            if qy[0] == "!=":
                return data[data[field] != qy[1]]
            if qy[0] == ">":
                return data[data[field] > qy[1]]
            if qy[0] == ">=":
                return data[data[field] >= qy[1]]
            if qy[0] == "<=":
                return data[data[field] <= qy[1]]
            if qy[0] == "<":
                return data[data[field] < qy[1]]

    # recursive cases: when there are some 'and' or 'or'
    else:
        # we first deal with or because in python 'and' has the priority: must be dealt with last. 
        # Ex 'x or y and z' will be dealt as [x, y and z] first, to make sure that 'y and z' will be evaluated. Otherwise, it would be (x or y) and z
        if re.search(r'(\sor\s)', query):   
           
        # splits the query and removes the 'or'
            splitted = query.split(' or ')
           
        # This time the two recursions are done separately and joined in the return statement
            left = do_filter_by_value(data, splitted[0], field)   
            # The .join function is to treat a query with multiple 'or' inside and treats them one after the other.
            right = do_filter_by_value(data, ' or '.join(splitted[1:]), field)
            # how = 'outer': every row from the left and right dataframes is retained in the result. 
            return left.merge(right, how='outer')
           
        # if the first one is an 'and'
        if re.search(r'(\sand\s)', query):
            # splits the query in two and removes 'and'
            splitted = query.split(' and ')
            
            # Double recursion
            # The .join function allows the query to have multiple 'and' inside and treats them one after the other.
            return do_filter_by_value(do_filter_by_value(data, splitted[0], field), ' and '.join(splitted[1:]), field)

        
date_dict = dict()  # this variable will store do_compute_date_column results for future use


def do_compute_date_column(row):  # input is always pd.Series (row of a pd.DataFrame)

    global date_dict
    timespan = row['timespan']           # store timespan in 'P_Y_M_D' format
    date_column_value = row['creation']  # store date of creation in 'YYYY-MM-DD' format

    # If creation is only a year add a few days to avoid weird calculations
    if str(date_column_value)[4:] == '-01-01 00:00:00':
        date_column_value = date_column_value + np.timedelta64('10', 'D')

    # 1. Base case: result already computed and in global dict
    if row['cited'] in date_dict:        
        return date_dict[row['cited']]
    
    # 2. Compute 'creation_cited' column value for the row in input
    else:                            

        negative = False                 # timespan is assumed to be positive
        if timespan[0] == "-":
            negative = True              # if negative, this variable will show that

        timespan = timespan.strip('PD')  # remove the 'P' at the beginning and the 'D' at the end of 'timespan'
        ls = re.split('[YM]', timespan)  # create a list in [yy, mm, dd] format for easier handling

        if not negative:                 # a. Timespan is POSITIVE: compute by subtraction
            for idx, value in enumerate(ls):  # loop through elements in list 'ls' (could be YY, YY-MM or YY-MM-DD)
                if idx == 0:                    # compute year
                    date_column_value = date_column_value - np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # compute month
                    date_column_value = date_column_value - np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # compute day
                    date_column_value = date_column_value - np.timedelta64(value, 'D')

        else:                            # b. Timespan is NEGATIVE: compute by addition
            for idx, value in enumerate(ls):  # loop through elements in list 'ls' (could be YY, YY-MM or YY-MM-DD)
                if idx == 0:                    # compute year
                    date_column_value = date_column_value + np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # compute month
                    date_column_value = date_column_value + np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # compute day
                    date_column_value = date_column_value + np.timedelta64(value, 'D')
        
        # 3. Store result for future use: only save year as month and day could be slightly wrong due to time handling
        date_dict[row['cited']] = date_column_value.date().year   
        
        return date_dict[row['cited']]
    
    
