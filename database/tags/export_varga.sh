#!/usr/local/bin/python

# todo: write a parametrized vrsion of the query below

.mode csv
.output output_mula_svargavarga.csv
select sloka_number, sloka_line, sloka_text from mula where varga='स्वर्गवर्गः' order by id;
.quit
