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

    for doi in dois: # loop through input DOIs

        cited = data.set_index('cited')   # save data indexed by 'cited' column to local variable
        try:                              # handle KeyError exception
            creation = cited.loc[doi]['creation']  # this can either be a str or a pandas series
            if type(creation) == pandas.core.series.Series: # if series, loop through rows
                for i in creation:
                    if i[:4] == year:
                        cit_counter += 1
            elif type(creation) == str:                     # otherwise just compare year of creation and input year
                if creation[:4] == year:
                    cit_counter += 1
        except KeyError:
            pass

        citing = data.set_index('citing')  # save data indexed by 'citing' column to local variable
        try:                               # handle KeyError exception
            creation = citing.loc[doi]['creation']  # this can either be a str or a pandas series
            if type(creation) == pandas.core.series.Series:
                if int(creation.iloc[1][:4]) == (int(year))-1 or int(creation.iloc[0][:4]) == (int(year))-2:
                    print('DEBUG: ', creation.iloc[0][:4], 'is == to either {} or {}'.format(str(int(year)-1), str(int(year)-2)))
                    pub.add(doi)
            elif type(creation) == str:
                if int(creation[:4]) == (int(year))-1 or (int(year))-2:
                    print('DEBUG: ', creation[:4], 'is == to either {} or {}'.format(str(int(year)-1), str(int(year)-2)))
                    pub.add(doi)
        except KeyError:
            pass

    try:
        return 'numeratore {}, denominatore {}, if {}'.format(cit_counter, len(pub), round(cit_counter / len(pub), 2))
    except ZeroDivisionError:
        return 'ERROR:\n' \
               'Could not compute Impact Factor, no DOI was created in y-1 or y-2\n' \
               'please try with another year\n' \
               '[encountered ZeroDivisionError] {}'.format(cit_counter)



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

