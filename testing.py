############################################################################################
#                                   PANDAS version                                         #
import pandas

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 800)

f = '/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'


def process_citations_pandas(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype="string")
    return data_frame


def do_compute_impact_factor(data, dois, year):  # dois is a set, year is 4 digit string 'YYYY'

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
        return "Could not compute impact factor: no DOIs pointed to objects published in \n" \
               "year-1 or year-2. Please try with another input set or year."



print(do_compute_impact_factor(process_citations_pandas(f),
                               {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                '10.1097/mop.0000000000000929', # created 2020 N
                                '10.1177/000313481107700711',   # created 2011 N
                                '10.3414/me14-05-0004',         # created 2014 Y
                                '10.3928/01477447-20180123-06', # created 2018 N
                                '10.1002/ddr.21369',            # created 2016 N
                                '10.3889/mmej.2015.50002',      # created 2015 Y
                                '10.1016/s0140-6736(97)11096-0'}, # no creation
                               '2016'))
print(do_compute_impact_factor(process_citations_pandas(f),
                               set(), '2016'))
print(do_compute_impact_factor(process_citations_pandas(f),
                                {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                '10.1097/mop.0000000000000929', # created 2020 N
                                '10.1177/000313481107700711',   # created 2011 N
                                '10.3414/me14-05-0004',         # created 2014 Y
                                '10.3928/01477447-20180123-06', # created 2018 N
                                '10.1002/ddr.21369',            # created 2016 N
                                '10.3889/mmej.2015.50002',      # created 2015 Y
                                '10.1016/s0140-6736(97)11096-0'},
                                2016))

#####################################################################################
#                               digraph version                                     #


import csv
from networkx import DiGraph


def process_citations(citations_file_path):
    g = DiGraph()  # creates directed graph

    with open(citations_file_path, mode="r") as csv_file:  # opens csv in read-mode
        reader = csv.DictReader(csv_file)

        for row in reader:    # loop through rows, each row representing a citation

            g.add_node(row['citing'], creation=row['creation'])  # creates citing node w/ attribute 'creation'

            g.add_node(row['cited'])                             # creates cited node

            g.add_edge(row['citing'], row['cited'], timespan=row['timespan'])  # creates edge w/ attribute 'timespan'

    return g  # might be better to return adjacency dict (.adj) or a tuple of (nodes, edges)


def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'
    # data is in DiGraph format

    cit_counter = 0  # this will be the dividend
    pub = set()          # this will be the divisor

    for doi in dois:
        citing = data.predecessors(doi)  # this is the network of articles citing a given DOI
        for identifier in list(citing):
            if str(data.nodes[identifier]['creation'][:4]) == year:
                cit_counter += 1  # keeps count of citations in given year

        try:   # python raises a KeyError when node doesn't have a creation date, handle it with exception
            if data.nodes[doi]['creation'][:4] == str(int(year)-1) or data.nodes[doi]['creation'][:4] == str(int(year)-2):
                pub.add(doi)          # keeps count of the DOIs published in y-1 and y-2
        except KeyError:
            pass

    return round((cit_counter / len(pub)), 2)