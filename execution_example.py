# -*- coding: utf-8 -*-
# Copyright (c) 2020, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

# import the class 'BibliometricEngine' from the local file 'bibengine.py'
from bibengine import BibliometricEngine
from networkx import draw_networkx
import matplotlib.pyplot as plt


#testing files: ~/Desktop/testing_csv.csv OR citations_sample.csv

# create a new object of the class 'BibliometricEngine' specifying the input CSV files to process
my_be = BibliometricEngine('citations_sample.csv')
# the data in the object can be accessed through the .data method specified in the __init__ function
#print(my_be.data[my_be.data['citing'].isin({'10.3389/fpsyg.2016.01483', '10.1097/mop.0000000000000929', '10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'})])

#
# for i in range(2001, 2020):
#     print("------\n{}".format(i))
#     print(my_be.compute_impact_factor({'10.3389/fpsyg.2016.01483', '10.1097/mop.0000000000000929', '10.1177/000313481107700711','10.3414/me14-05-0004','10.3928/01477447-20180123-06','10.1002/ddr.21369','10.3889/mmej.2015.50002','10.1016/s0140-6736(97)11096-0'}, str(i)))

# for i in range(2001, 2020):
#     print("-------------------------------------------------------")
#     print(i)
#     print(my_be.compute_impact_factor({'federico', 'giulia', 'ivan', 'luisa', 'constance', 'bruno'}, str(i)))


graph = my_be.get_citation_network(2010, 2018)
draw_networkx(graph, with_labels=True)
plt.show()
