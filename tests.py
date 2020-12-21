import csv

def process_citations(citations_file_path):
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


citations = process_citations("citations_sample.csv")
# print(citations)
# print(test_do_compute_impact_factor(citations, set(['10.1016/s0140-6736(97)11096-0','10.1001/archpediatrics.2009.42','10.1097/mop.0000000000000929']),'2020', 59))
print(do_compute_impact_factor(citations, set(get_all_citing(citations)), '2013'))

