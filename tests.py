import csv
import pandas as pd
import re



#my code before pandas
def process_citations_base(citations_file_path):
    # dict_cit = dict()
    matrix = list()

    with open(citations_file_path, mode='r', encoding='utf-8') as file:
        # csvFile = csv.reader(file, delimiter=',')
        # next(csvFile)
        # for line in csvFile:
        #     matrix.append(line)
        csvFile = csv.DictReader(file)
        # for line in csvFile:
        #     if line['citing'] not in dict_cit:
        #         dict_cit[(line['citing'], line['creation'])]=[(line['cited'], line['timespan'])]
        #     else:
        #         dict_cit[(line['citing'], line['creation'])].append((line['cited'], line['timespan']))
        for line in csvFile:
            matrix.append(line)
    return matrix

def test_do_compute_impact_factor(data, dois, year, expected):
    return do_compute_impact_factor(data, dois, year) == expected

def get_all_citing(data):
    result=[]
    for line in data:
        result.append(line['citing'])
    return result

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
# print(citations)
# print(test_do_compute_impact_factor(citations, set(['10.1016/s0140-6736(97)11096-0','10.1001/archpediatrics.2009.42','10.1097/mop.0000000000000929']),'2020', 59))
#print(do_compute_impact_factor(citations, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, '2016'))

def process_citations_pandas(citations_file_path):
    return pd.read_csv(citations_file_path, encoding='utf-8')

citations_pandas = process_citations_pandas('citations_sample.csv')
#print(citations)

# Very useful to see the infos about the table: especially for the efficiency -> memory usage
# print(data.info())

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
    denom = set()

    for doi in dois:
        print(data.query('citing.to_string == {}'.format(doi)))

    return round(num / len(denom), 2)


#print(do_compute_impact_factor_pandas(citations_pandas, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, '2016'))
#print(do_compute_impact_factor_pandas_two(cit_pandas_dates, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, '2016'))
#print(do_compute_impact_factor(citations, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, '2016'))


#the function is working, but can't be used with 'creation' as Date format, I have to find a way to deal with it
def do_search(data, query, field):

    #preliminary verifications on the data provided
    if type(query) is not str or query == '':
        return 'Please provide a valid string as a query'
    if field not in data.columns:
        return 'Please provide a valid field for the data'

    #base case: if there are no operators expcept 'not'
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

            if field == "creation":
                return data[data[field].dt.strftime("%Y-%m-%d").str.count(result)==0]
            else:
                #selects only the rows where the statement is not true on the column 'field'
                return data[data[field].str.count(result)==0]
        elif field == "creation":
            print(result)
            return data[data[field].dt.strftime("%Y-%m-%d").str.count(result)>0]

        else:
            print(result)
            # else selects only the rows where the query returns true on the column 'field'
            return data[data[field].str.count(result)>0]

    #recursive cases: when there are some 'and' or 'or'
    else:

        # we first deal with or because in python 'and' has the priority: must be dealt with last
        # for example: True or True and False = True or (True and False) = True or False = True
        # an example for our data: x or y and z will be dealt as [x, y and z] first, to make sure that 'y and z' will be evaluated.
        # otherwise, it would be (x or y) and z and we don't want that
        if re.search(r'(\sor\s)', query):

            #splits the query in two and removes the 'or'
            splitted = query.split(' or ')
            print("there's an 'or':", splitted)

            #This time the two recursions are done separately and joined in the return statement
            left = do_search(data, splitted[0], field)
            #The .join function is to treat a query with multiple 'or'
            right = do_search(data, ' or ' .join(splitted[1:]), field)

            #how = 'outer' uses the union of keys from both Dataframes. Attention: the keys are not mainained
            return left.merge(right, how='outer')
            # if the first one is an 'and'

        if re.search(r'(\sand\s)', query):

            # splits the query in two and removes 'and'
            splitted = query.split(' and ')
            print("there's an 'and':",splitted)
            # in this line there are two recursions: the data provided to the second part of the query
            # is the one returned by the call of this function on the first part.
            # The .join function allows the query to have multiple 'and' inside and treats them one after the other.
            return do_search(do_search(data, splitted[0], field), ' and '.join(splitted[1:]), field)

# print(do_search(cit_pandas_dates, 2, 'citing'))
# print(do_search(cit_pandas_dates, 'hello', 'cit'))
# print(do_search(cit_pandas_dates, 'ArcHdischIld', 'citing'))
# print("Doing the search for '-01 and not 2008' :\n", do_search(cit_pandas_dates, '-01 and not 2008', 'creation'))
# print("Doing the search for '2007 or not 2008 and -01 or -02' :\n", do_search(cit_pandas_dates, '2007 or not 2008 and -01 or -02', 'creation'))
# print("Doing the search for '10.1057*biosoc' :\n", do_search(cit_pandas_dates, '10.1057*biosoc', 'citing'))
# print("Doing the search for '01461672 and 115' :\n", do_search(cit_pandas_dates, '01461672 and 115', 'cited'))

def do_search_by_prefix(data, prefix, is_citing):
    #defining the query to do on the fields using Regex
    query = prefix+'/.*'

    #deciding on which field to do the query
    if is_citing:
        field = 'citing'
    else:
        field = 'cited'

    #returning a subcollection of the data where the query on the right field is true
    return data[data[field].str.count(query)>0]

# print(do_search_by_prefix(cit_pandas_dates, '10.3390', True))
# print(do_search_by_prefix(cit_pandas_dates, '10.1016', False))


def do_filter_by_value(data, query, field):
    if type(query) is not str or query == '':
        return 'Please provide a valid string as a query'
    if field not in data.columns:
        return 'Please provide a valid field for the data'
    # base case: if there is no 'and' or 'or'.
    if not re.search(r'(\sand\s|\sor\s)', query):
        if " " not in query:
            return data[data[field] == query]
        else:
            qy = query.split(' ')  # ["==", "2001"]
            if qy[0] == "==":  # "== > < != >= <=": #base case "2001" "== 2001"
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
        # creates a list with all the operators from left to right
        found = re.findall(r'\sand\s|\sor\s', query)
        # if the first one is an 'and'
        if found[0] == ' and ':
            print("there's an 'and'")
            # splits the query in two and removes 'and': splitted è una LIST
            splitted = query.split(' and ')

            # The .join function allows the query to have multiple 'and' inside and treats them one after the other.
            return do_filter_by_value(do_filter_by_value(data, splitted[0], field), ' and '.join(splitted[1:]), field)
        # if the first one is an 'or'
        if found[0] == ' or ':
            print("there's an 'or'")
            # splits the query in two and removes the 'or'
            splitted = query.split(' or ')
            # This time the two recursions are done separately and joined in the return statement
            left = do_filter_by_value(data, splitted[0], field)
            # The .join function is to treat a query with multiple 'or'
            right = do_filter_by_value(data, ' or '.join(splitted[1:]), field)
            # how = 'outer' uses the union of keys from both Dataframes. Attention: the keys are not mainained
            return left.merge(right, how='outer')

print("Doing the search for '> 2007 and < 2010' :\n", do_filter_by_value(cit_pandas_dates, '> 2007 and < 2010', 'creation'))
