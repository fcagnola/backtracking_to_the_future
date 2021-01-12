setup = '''
import csv
import pandas as pd
import re



#my code before pandas
def process_citations_base(citations_file_path):
    with open(citations_file_path, mode='r', encoding='utf-8') as file:
        matrix = list()
        csvFile = csv.DictReader(file)
        for line in csvFile:
            matrix.append(line)
    return matrix

def do_compute_impact_factor(data, dois, year):

    #variables for counting the number of citations and the number of articles in the previous years
    num_citations = 0
    num_published_prec_years = 0
    
    #turning the year into an integer to substract easily
    year_int = int(year)

    #iterating over all the data and all the dois
    for doi in dois:
        for line in data:

            #checks if the doi has been cited in year 'year'
            if doi == line['cited'] and year == line['creation'][:4]:
                num_citations += 1

            #checks if the doi is a citing article and has been published in the previous two years
            if doi == line['citing'] and (line['creation'][:4] == str(year_int-1) or line['creation'][:4] == str(year_int-2)):
                num_published_prec_years += 1

    #return IF
    return num_citations/num_published_prec_years

citations = process_citations_base("citations_sample.csv")

def process_citations_pandas(citations_file_path):
    return pd.read_csv(citations_file_path, encoding='utf-8')

citations_pandas = process_citations_pandas('citations_sample.csv')


def process_citations_pandas_date(citations_file_path):
    data_frame = pd.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str}, parse_dates=['creation'])
    return data_frame

cit_pandas_dates = process_citations_pandas_date('citations_sample.csv')

def do_compute_impact_factor_pandas(data, dois, year):
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

def do_compute_impact_factor_pandas_two(data, dois, year):
    num = 0
    denom = 0

    for doi in dois:
        for row in data.index:
            if data['cited'][row] == doi and data['creation'][row].year == int(year):
                num += 1
            if data['citing'][row] == doi and (data['creation'][row].year == int(year)-1 or data['creation'][row].year == int(year)-2):
                denom += 1

    return round(num / denom, 2)
    
def do_search(data, query, field):

    #preliminary verifications on the data provided
    if type(query) is not str or query == '':
        return 'Please provide a valid string as a query'
    if field not in data.columns:
        return 'Please provide a valid field for the data'

    #base case: if there is no 'and' or 'or'
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

            #selects only the rows where the statement is not true on the column 'field'
            return data[data[field].str.count(result)==0]
        else:
            print(result)
            # else selects only the rows where the query returns true on the column 'field'
            return data[data[field].str.count(result)>0]

    #recursive cases: when there are some 'and' or 'or'
    else:

        #creates a list with all the operators from left to right
        found = re.findall(r'\sand\s|\sor\s', query)

        #if the first one is an 'and'
        if found[0] == ' and ':
            print("there's an 'and'")

            #splits the query in two and removes 'and'
            splitted = query.split(' and ')

            # in this line there are two recursions: the data provided to the second part of the query
            # is the one returned by the call of this function on the first part.
            # The .join function allows the query to have multiple 'and' inside and treats them one after the other.
            return do_search(do_search(data, splitted[0], field), ' and '.join(splitted[1:]), field)

        # if the first one is an 'or'
        if found[0] == ' or ':
            print("there's an 'or'")

            #splits the query in two and removes the 'or'
            splitted = query.split(' or ')

            #This time the two recursions are done separately and joined in the return statement
            left = do_search(data, splitted[0], field)
            #The .join function is to treat a query with multiple 'or'
            right = do_search(data, ' or ' .join(splitted[1:]), field)

            #how = 'outer' uses the union of keys from both Dataframes. Attention: the keys are not mainained
            return left.merge(right, how='outer')
            
def do_get_co_citations_consti(data, doi1, doi2):   #doi1 and doi2 are strings identifying 2 different 'cited' article
    if doi1 == doi2:
        return 'Please change one of the DOIs inserted'
    data_doi1_doi2 = data[["citing","cited"]].loc[data['cited'].isin([doi1, doi2])]  # a Dataframe (with 2 columns) cointaining only the rows with doi1 and doi2 in 'cited' column
    # if a 'citing' document is repeat twice that means it cites both doi1 and doi2 articles (which are the only taken into account by the 'data_doi1_doi2' DataFrame
    data_duplicated_values = data_doi1_doi2[data_doi1_doi2.duplicated(subset=['citing'])]  #'drop_duplicate' removes duplicates on specific column(s) declared by 'subset'.

    if len(data_duplicated_values)==0: #that means that 'drop_duplicates' did not find any duplicated value, so any co-citations
        return "The doi1 and doi2 are never cited together by other documents"
    else:
        return len(data_duplicated_values) #detecting how many values (duplicated) have been removed

def do_get_co_citations_lu(data, doi1, doi2):   #doi1 and doi2 are strings identifying 2 different 'cited' article
    if doi1 == doi2:
        return 'Please change one of the DOIs inserted'
    data_doi1_doi2 = data[["citing","cited"]].loc[data['cited'].isin([doi1, doi2])]  # a Dataframe (with 2 columns) cointaining only the rows with doi1 and doi2 in 'cited' column
    # if a 'citing' document is repeat twice that means it cites both doi1 and doi2 articles (which are the only taken into account by the 'data_doi1_doi2' DataFrame
    data_less_duplicated_values = data_doi1_doi2.drop_duplicates(subset=['citing'])  #'drop_duplicate' removes duplicates on specific column(s) declared by 'subset'.

    if len(data_doi1_doi2) == len(data_less_duplicated_values): #that means that 'drop_duplicates' did not find any duplicated value, so any co-citations
        return "The doi1 and doi2 are never cited together by other documents"
    else:
        return len(data_doi1_doi2) - len(data_less_duplicated_values) #detecting how many values (duplicated) have been removed
'''

import timeit


def singleevaluator(setup, statement, number=1000):
    a = timeit.timeit(setup=setup, stmt=statement, number=number)
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


l_statements = ['''do_get_co_citations_consti(citations_pandas,"10.1177/2372732215600716", "10.1016/s0140-6736(97)11096-0") ''', '''do_get_co_citations_lu(citations_pandas,"10.1177/2372732215600716", "10.1016/s0140-6736(97)11096-0")''']
l_functions = ['do_get_co_citations_consti()', 'do_get_co_citations_lu()']

print(multipleniceevaluator(l_functions, setup, l_statements))









credits = ''' the algorithm takes inspiration from
the functions described here: https://www.studytonight.com/post/calculate-time-taken-by-a-program-to-execute-in-python#'''