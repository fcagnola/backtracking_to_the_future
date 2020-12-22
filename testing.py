# PANDAS version
import pandas

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 800)

f = '/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'


def process_citations_pandas(citations_file_path):
    data_frame = pandas.read_csv(citations_file_path)
    return data_frame


def do_compute_impact_factor(data, dois, year):  # dois is a set, year is 4 digit string 'YYYY'

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
    return 'numeratore {}, denominatore {}, if {}'.format(cit_counter, len(pub), round(cit_counter/len(pub), 2))


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

