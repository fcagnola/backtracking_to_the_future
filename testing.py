############################################################################################
#                                   PANDAS version                                         #
import pandas

pandas.set_option('display.max_columns', 5)
pandas.set_option('display.width', 800)

f = '/Users/federicocagnola/PycharmProjects/backtracking_to_the_future/citations_sample.csv'


def process_citations(citations_file_path):
    # processing through pandas' read.csv function: date parsing is necessary for easier handling of 'creation' column
    data_frame = pandas.read_csv(citations_file_path, dtype={'citing': str, 'cited': str, 'timespan': str}, parse_dates=['creation'])
    return data_frame


def do_compute_impact_factor(data, dois, year):  # DOIs is a set, year is 4 digit string 'YYYY'

    # input validation
    if len(dois) == 0:
        return 'Please insert a valid set of DOIs'
    if type(year) == int:
        return 'Please provide a year in string format: "YYYY"'

    num = 0         # numerator for the final computation
    denom = 0       # denominator for the final computation

    # selecting only citations by documents published in year 'year'
    data_year = data.loc[data['creation'].dt.year == int(year)]

    # selecting only citations with previous two years: concatenate
    data_previous_two_years = pandas.concat([data.loc[data['creation'].dt.year == (int(year) - 1)], data.loc[data['creation'].dt.year == (int(year) - 2)]])

    for doi in dois:
        # selecting rows with doi == cited and adding the length of this table to num
        data_year_cited = data_year.loc[data_year['cited'] == doi]
        num += len(data_year_cited)

        # selecting rows with doi == citing and adding the length of this table to denom
        data_previous_years_citing = data_previous_two_years.loc[data_previous_two_years['citing'] == doi]
        denom += len(data_previous_years_citing)

    try:
        return round(num / denom, 2)
    except ZeroDivisionError:
        return "Could not compute impact factor: no DOIs pointed to objects published in \n" \
               "year-1 or year-2. Please try with another input set or year."


# FOR TESTING PANDAS VERSION UNCOMMENT THE FOLLOWING LINES

print(do_compute_impact_factor(process_citations(f),
                               {'10.3389/fpsyg.2016.01483',     # created 2016 N
                                '10.1097/mop.0000000000000929', # created 2020 N
                                '10.1177/000313481107700711',   # created 2011 N
                                '10.3414/me14-05-0004',         # created 2014 Y
                                '10.3928/01477447-20180123-06', # created 2018 N
                                '10.1002/ddr.21369',            # created 2016 N
                                '10.3889/mmej.2015.50002',      # created 2015 Y
                                '10.1016/s0140-6736(97)11096-0'}, # no creation
                               '2016'))
print(do_compute_impact_factor(process_citations(f),
                               set(), '2016'))
print(do_compute_impact_factor(process_citations(f),
                                {'10.3389/fpsyg.2016.01483',    # created 2016 N
                                '10.1097/mop.0000000000000929', # created 2020 N
                                '10.1177/000313481107700711',   # created 2011 N
                                '10.3414/me14-05-0004',         # created 2014 Y
                                '10.3928/01477447-20180123-06', # created 2018 N
                                '10.1002/ddr.21369',            # created 2016 N
                                '10.3889/mmej.2015.50002',      # created 2015 Y
                                '10.1016/s0140-6736(97)11096-0'},
                                2016))
print(do_compute_impact_factor(process_citations(f),
                               {'10.1007/s00134-019-05862-0',   # created 2019
                                '10.1097/mop.0000000000000929', # created 2020
                                '10.3389/fpsyg.2016.01483',     # created 2016
                                '10.1007/s40506-020-00219-4',   # created 2020
                                '10.1002/1097-0355(200101/04)22:1<132::aid-imhj5>3.0.co2-9'},
                               '2018'))

