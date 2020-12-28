from test_efficiency import *

#setup =
import csv
import pandas as pd



#my code before pandas
def process_citations_base(citations_file_path):
    # dict_cit = dict()
    with open(citations_file_path, mode='r', encoding='utf-8') as file:
        matrix = list()
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

citations = process_citations_pandas('citations_sample.csv')
#print(citations)

# Very useful to see the infos about the table: especially for the efficiency -> memory usage
# print(data.info())

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

print(do_compute_impact_factor_pandas(citations, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, '2016'))

# l_statements = ['''do_compute_impact_factor(citations, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, '2016')''', '''do_compute_impact_factor_pandas(citations, {'10.3389/fpsyg.2016.01483','10.1097/mop.0000000000000929','10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, '2016')''']
# l_functions = ['do_compute_impact_factor()', 'do_compute_impact_factor_pandas()']
#
# print(multipleniceevaluator(l_functions, setup, l_statements))
