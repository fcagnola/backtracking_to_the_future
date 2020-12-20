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
    return do_compute_impact_factor(data, dois, year)==expected

def do_compute_impact_factor(data, dois, year):
    num_citations = 0
    num_published_prec_years = 0
    for doi in dois:
        for line in data:
            if doi == line['cited'] and year == line['creation'][:4]:
                num_citations +=1


    return num_citations

citations = process_citations("citations_sample.csv")
print(citations)
print(do_compute_impact_factor(citations, set(['10.1016/s0140-6736(97)11096-0']),'2011'))