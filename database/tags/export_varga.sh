#!/usr/local/bin/python

# todo: write a parametrized vrsion of the query below

.mode csv
.output output_mula_kalavarga.csv
select sloka_number, sloka_line, sloka_text from mula where varga='कालवर्गः' order by id;
.quit
