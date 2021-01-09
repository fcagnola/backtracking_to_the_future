# EFFICIENCY TESTING:
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


setup = '''
import pandas
import numpy as np
import re

def process_citations(citations_file_path):  # years in 'YYYY' format should be 'YYYY-01-05'
    # processing through pandas' read.csv function: date parsing is necessary for easier handling of 'creation' column
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str},
                                 parse_dates=['creation'])
    return data_frame

dataframe = process_citations('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv')


'''
l_statements = ['''
date_dict = dict()
dataframe['creation_cited'] = dataframe[['cited', 'creation', 'timespan']].apply(do_compute_date_column, axis=1)
''']
l_functions = ["do_compute_date_column()"]

#######################################################################################################################



date_dict = dict()
print(multipleniceevaluator(l_functions, setup, l_statements, 100))
