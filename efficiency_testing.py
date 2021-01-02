# EFFICIENCY TESTING:


setup = '''
import pandas
from networkx import DiGraph, from_pandas_edgelist
import numpy as np
import re

def process_citations(citations_file_path):
    # processing through pandas' read.csv function: date parsing is necessary for easier handling of 'creation' column
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str}, parse_dates=['creation'])
    return data_frame

dataframe = process_citations('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv')

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

    return date_column_value
'''
l_statements = ['''do_get_citation_network(dataframe, "2018", "2020")''']
l_functions = ["do_get_citation_network()"]

#######################################################################################################################

import timeit


def singleevaluator(setup, statement, number=1000):
    a = timeit.timeit(setup=setup, stmt= statement, number=number)
    return a


def multipleniceevaluator(listoffunctions, setup, listofstatements, number=1000):
    if len(listoffunctions) == len(listofstatements):
       listofextimes = []
       for el in listoffunctions:
           time = singleevaluator(setup, listofstatements[listoffunctions.index(el)], number)
           listofextimes.append(time)
           print("The execution time of function " + el + " is " + str(time))
       print("The most efficient function is " + str(listoffunctions[listofextimes.index(min(listofextimes))]) +
             " that runs in " + str(min(listofextimes)) + " seconds.")
       print("The least efficient function is " + str(listoffunctions[listofextimes.index(max(listofextimes))]) +
             " that runs in " + str(max(listofextimes)) + " seconds.")
    else:
        print("Invalid input, the length of the lists you have put as input is different")


print(multipleniceevaluator(l_functions, setup, l_statements, 100))
