############################################################################################
#                                   PANDAS version                                         #
import pandas
import re
import numpy as np

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 800)

f = '/Users/federicocagnola/Desktop/testing_csv.csv'


def process_citations(citations_file_path):
    # processing through pandas' read.csv function: date parsing is necessary for easier handling of 'creation' column
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str}, parse_dates=['creation'])
    return data_frame

df = process_citations(f)

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

    return date_column_value.date().year


df['creation_cited'] = df[['creation', 'timespan']].apply(do_compute_date_column, axis=1)
print(df)
