import pandas

f = 'citations_sample.csv'

def process_citations_pandas(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path, dtype=str)
    return data_frame

def do_compute_impact_factor(data, dois, year):  # dois is a set, year is 4 digit string 'YYYY'
    cit_counter = 0  # dividend
    pub = 0          # divisor

    citing = data['citing']
    c_year = data['creation']
    print(data.head())
    for doi in dois:
        if doi in citing:

            if c_year == year:
                cit_counter += 1
            if c_year:
                pass




print(do_compute_impact_factor(process_citations_pandas(f), {'10.1007/s00134-019-05862-0', '10.3390/vaccines7040201', '10.3390/vaccines8040600',
                                  '10.3414/me14-05-0004'}, 2019))