# EFFICIENCY TESTING: PANDAS VS NETWORKX DATA STRUCTURE

# RESULTS:
# The execution time of function impact_factor_fede() is 9.074071624
# The execution time of function impact_factor_constance() is 3.8846544460000008
# The most efficient function is impact_factor_constance() that runs in 3.8846544460000008 seconds.
# The least efficient function is impact_factor_fede() that runs in 9.074071624 seconds.

setup = '''
import pandas

def process_citations(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype="string")
    return data_frame

dataframe = process_citations('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv')

def process_citations_date(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str},
                                 parse_dates=['creation'])
    return data_frame

df = process_citations_date('/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv')

def impact_factor_fede(data, dois, year):  # dois is a set, year is 4 digit string 'YYYY'

    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'
    cit_counter = 0                             # value will be dividend
    pub = set()                                 # len will be divisor

    for doi in dois:                            # loop through input DOIs

        data.set_index('cited', inplace=True)   # index dataframe by 'cited' column
        try:
            created = data.loc[doi, 'creation'] # lookup all mentions of the DOI in the input set, column 'creation'
            for i in created:
                if i[:4] == year:
                    cit_counter += 1
        except KeyError:
            pass
        data.reset_index(inplace=True)          # reset original integer index

        data.set_index('citing', inplace=True)  # index dataframe by 'citing' column

        try:
            creation = data.loc[doi, 'creation'][0] # select creation year of the first match (all rows will be identical)

            if len(creation) == 1:  # if result was a single row, creation contains only '2', the first char of 'YYYY'
                creation = data.loc[doi, 'creation'][:4]                      # correct problem of the line before

            if creation == str(int(year)-1) or creation == str(int(year)-2):
                pub.add(doi)
        except KeyError:
            pass
        data.reset_index(inplace=True)          # reset original integer index
    try:
        return round(cit_counter/len(pub), 2)
    except ZeroDivisionError:
        return "Could not compute impact factor: no DOIs pointed to objects published in "\n" year-1 or year-2. Please try with another input set or year."
               
def impact_factor_constance(data, dois, year):
    num = 0
    denom = 0
    
    # selecting only rows with year 'year'
    data_year = data.loc[data['creation'].str.contains(year)]

    #selecting only rows with previous two years
    data_previous_two_years = data.loc[data['creation'].str.contains(str(int(year)-1)+'|'+str(int(year)-2))]
    for doi in dois:

        #selecting rows with doi == cited and adding the length of this table to num
        data_year_cited = data_year.loc[data_year['cited'] == doi]
        num += len(data_year_cited)

        #selecting rows with doi == citing and adding the length of this table to denom
        data_previous_years_citing = data_previous_two_years.loc[data_previous_two_years['citing'] == doi]
        denom += len(data_previous_years_citing)

    return round(num/denom, 2)

def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'
    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'

    num = 0
    denom = 0

    # selecting only rows with year 'year'
    data_year = data.loc[data['creation'].dt.year == int(year)]

    # selecting only rows with previous two years
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
        return "Could not compute impact factor: no DOIs pointed to objects published in year-1 or year-2. Please try with another input set or year."
'''
l_statements = ['''impact_factor_fede(dataframe, {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                '10.1097/mop.0000000000000929', # created 2020 N
                                '10.1177/000313481107700711',   # created 2011 N
                                '10.3414/me14-05-0004',         # created 2014 Y
                                '10.3928/01477447-20180123-06', # created 2018 N
                                '10.1002/ddr.21369',            # created 2016 N
                                '10.3889/mmej.2015.50002',      # created 2015 Y
                                '10.1016/s0140-6736(97)11096-0'}, "2016")''',
                '''impact_factor_constance(dataframe, {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                '10.1097/mop.0000000000000929', # created 2020 N
                                '10.1177/000313481107700711',   # created 2011 N
                                '10.3414/me14-05-0004',         # created 2014 Y
                                '10.3928/01477447-20180123-06', # created 2018 N
                                '10.1002/ddr.21369',            # created 2016 N
                                '10.3889/mmej.2015.50002',      # created 2015 Y
                                '10.1016/s0140-6736(97)11096-0'}, "2016")''',
                '''do_compute_impact_factor(df, {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                '10.1097/mop.0000000000000929', # created 2020 N
                                '10.1177/000313481107700711',   # created 2011 N
                                '10.3414/me14-05-0004',         # created 2014 Y
                                '10.3928/01477447-20180123-06', # created 2018 N
                                '10.1002/ddr.21369',            # created 2016 N
                                '10.3889/mmej.2015.50002',      # created 2015 Y
                                '10.1016/s0140-6736(97)11096-0'}, "2016")''']
l_functions = ["impact_factor_fede()", "impact_factor_constance()", "do_compute_impact_factor()"]

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


print(multipleniceevaluator(l_functions, setup, l_statements, 500))
