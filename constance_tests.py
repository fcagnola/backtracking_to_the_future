import csv

def process_citations(citations_file_path):
    dict_cit = dict()
    with open(citations_file_path, mode='r', encoding='utf-8') as file:
        # csvFile = csv.reader(file, delimiter=',')
        # next(csvFile)
        # for line in csvFile:
        #     matrix.append(line)
        csvFile = csv.DictReader(file)
        for line in csvFile:
            if line['citing'] not in dict_cit:
                dict_cit[(line['citing'], line['creation'])]=[(line['cited'], line['timespan'])]
            else:
                dict_cit[(line['citing'], line['creation'])].append((line['cited'], line['timespan']))
    return dict_cit


def do_compute_impact_factor():
    return

citations = process_citations("citations_sample.csv")
for key,value in citations.items():
    print(key, value)