# EFFICIENCY TESTING: PANDAS VS NETWORKX DATA STRUCTURE

# RESULTS:
# The execution time of function process_citations() is 7.062764464
# The execution time of function process_citations_pandas() is 2.307152372999999
# The most efficient function is process_citations_pandas() that runs in 2.307152372999999 seconds.
# The least efficient function is process_citations() that runs in 7.062764464 seconds.

setup = '''
import csv
from networkx import DiGraph
import pandas

def process_citations(citations_file_path):
    g = DiGraph()  # for citations a directed graph would be the best choice

    with open(citations_file_path, mode="r") as csv_file:  # opening csv in read-mode
        reader = csv.DictReader(csv_file)

        for row in reader:    # loop through rows, each row representing a citation
            g.add_node(row['citing'], creation=row['creation'])  # create the citing node, with attribute 'creation'
            g.add_node(row['cited'])                             # create cited node
            g.add_edge(row['citing'], row['cited'], timespan=row['timespan'])  # create edge with timespan as attribute

    return g  # i wonder if it would be better to return the adj dictionary or a tuple of (nodes, edges)

def process_citations_pandas(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype=str)
    return data_frame
'''
l_statements = ['''process_citations("/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv")''', '''process_citations_pandas("/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv")''']
l_functions = ['process_citations()', 'process_citations_pandas()']
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