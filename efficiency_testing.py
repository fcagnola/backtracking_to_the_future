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
date_dict = dict()  # this variable will store do_compute_date_column results for future use

def do_compute_date_column(row):  # input is always pd.Series (row of a pd.DataFrame)

    date_dict = dict()                     # allows to use global variable inside a function
    timespan = row['timespan']           # elem at index 'timespan' of the series is the timespan in 'P_Y_M_D' format
    date_column_value = row['creation']  # elem at index 'creation' is the date of creation in 'YYYY-MM-DD' format

    # if creation is only a year, add a few days to avoid weird calculations
    if str(date_column_value)[4:] == '-01-01 00:00:00':
        date_column_value = date_column_value + np.timedelta64('10', 'D')

    if row['cited'] in date_dict:        # base case: result already computed and in global dict
        return date_dict[row['cited']]

    else:                                # computation and storage for future use in the global dict

        negative = False                 # timespan is assumed to be positive
        if timespan[0] == "-":
            negative = True              # if negative, the appropriate variable will show that

        timespan = timespan.strip('PD')  # remove the 'P' at the beginning and the 'D' at the end of 'timespan'
        ls = re.split('[YM]', timespan)  # create a list in [yy, mm, dd] format for easier handling

        if not negative:                 # 1. Timespan is POSITIVE: compute by subtraction
            for idx, value in enumerate(ls):  # loop through elements in list 'ls' (could be YY, YY-MM or YY-MM-DD)
                if idx == 0:                    # first elem is always year: compute year
                    date_column_value = date_column_value - np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # second elem is always month: compute month
                    date_column_value = date_column_value - np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # third elem is always day: compute day
                    date_column_value = date_column_value - np.timedelta64(value, 'D')

        else:                            # 2. Timespan is NEGATIVE: compute by addition
            for idx, value in enumerate(ls):  # loop through elements in list 'ls' (could be YY, YY-MM or YY-MM-DD)
                if idx == 0:                    # first elem is always year: compute year
                    date_column_value = date_column_value + np.timedelta64(value, 'Y')
                elif idx == 1 and value != '':  # second elem is always month: compute month
                    date_column_value = date_column_value + np.timedelta64(value, 'M')
                elif idx == 2 and value != '':  # third elem is always day: compute day
                    date_column_value = date_column_value + np.timedelta64(value, 'D')

        date_dict[row['cited']] = date_column_value.date().year   # store result for future use, to speed up processing
        return date_dict[row['cited']]


'''
l_statements = ['''
date_dict = dict()
dataframe['creation_cited'] = dataframe[['cited', 'creation', 'timespan']].apply(do_compute_date_column, axis=1)
''']
l_functions = ["do_compute_date_column()"]

#######################################################################################################################



date_dict = dict()
print(multipleniceevaluator(l_functions, setup, l_statements, 100))
