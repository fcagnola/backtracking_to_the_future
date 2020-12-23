# EFFICIENCY TESTING: PANDAS VS NETWORKX DATA STRUCTURE

# RESULTS:
# The execution time of function process_citations() is 6.959494929
# The execution time of function process_citations_pandas() is 2.3277557140000003
# The most efficient function is process_citations_pandas() that runs in 2.3277557140000003 seconds.
# The least efficient function is process_citations() that runs in 6.959494929 seconds.

# The execution time of function do_compute_impact_factor() is 1.154579971
# The execution time of function do_compute_if_pandas() is 36.476305063
# The execution time of function do_compute_impact_factor_mx() is 1.3333440030000006
# The most efficient function is do_compute_impact_factor() that runs in 1.154579971 seconds.
# The least efficient function is do_compute_if_pandas() that runs in 36.476305063 seconds.


# setup = '''
# import csv
# from networkx import DiGraph
# import pandas
#
# def process_citations(citations_file_path):
#     g = DiGraph()  # creates directed graph
#
#     with open(citations_file_path, mode="r") as csv_file:  # opens csv in read-mode
#         reader = csv.DictReader(csv_file)
#
#         for row in reader:    # loop through rows, each row representing a citation
#
#             g.add_node(row['citing'], creation=row['creation'])  # creates citing node w/ attribute 'creation'
#
#             g.add_node(row['cited'])                             # creates cited node
#
#             g.add_edge(row['citing'], row['cited'], timespan=row['timespan'])  # creates edge w/ attribute 'timespan'
#
#     return g  # might be better to return adjacency dict (.adj) or a tuple of (nodes, edges)
#
# def process_citations_pandas(citations_file_path):
#     data_frame = pandas.read_csv(citations_file_path, dtype=str)
#     return data_frame
# '''
# l_statements = ['''process_citations("/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv")''', '''process_citations_pandas("/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv")''']
# l_functions = ['process_citations()', 'process_citations_pandas()']
#----------------------------------------------------------------------------------------------------------------------
setup = '''
from networkx import DiGraph
import csv
import pandas
f = '/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'

def process_citations(citations_file_path):
    g = DiGraph()  # creates directed graph

    with open(citations_file_path, mode="r") as csv_file:  # opens csv in read-mode
        reader = csv.DictReader(csv_file)

        for row in reader:    # loop through rows, each row representing a citation

            g.add_node(row['citing'], creation=row['creation'])  # creates citing node w/ attribute 'creation'

            g.add_node(row['cited'])                             # creates cited node

            g.add_edge(row['citing'], row['cited'], timespan=row['timespan'])  # creates edge w/ attribute 'timespan'

    return g  # might be better to return adjacency dict (.adj) or a tuple of (nodes, edges)
    
def process_citations_pandas(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path)
    return data_frame

def process_citations_matrix(citations_file_path):
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
    
c = process_citations(f)
cp = process_citations_pandas(f)
cx = process_citations_matrix(f)

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

def do_compute_if_pandas(data, dois, year):  # dois is a set, year is 4 digit string 'YYYY'

    cit_counter = 0  # value will be dividend
    pub = set()      # len will be divisor

    # this is the index of the columns of the dataframe, which keeps track of which row we're in
    for i in data.index:
        cited = data.loc[i, 'cited']
        citing = data.loc[i, 'citing']
        creation = data.loc[i, 'creation']
        for doi in dois:
            if doi == cited and creation[:4] == year:
                cit_counter += 1
            if doi == citing and creation[:4] == str(int(year)-1) or creation[:4] == str(int(year)-2):
                pub.add(doi)
    return round(cit_counter/len(pub), 2)

def do_compute_impact_factor_mx(data, dois, year):
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

'''
l_statements = ['''do_compute_impact_factor(c, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, 2016)''', '''do_compute_if_pandas(cp, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, 2016)''', '''do_compute_impact_factor_mx(cx, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, 2016)''']
l_functions = ['do_compute_impact_factor()', 'do_compute_if_pandas()', 'do_compute_impact_factor_mx()']
#----------------------------------------------------------------------------------------------------------------------
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

print(multipleniceevaluator(l_functions, setup, l_statements))