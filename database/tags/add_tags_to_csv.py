#!/usr/local/bin/python

import argparse, csv

parser = argparse.ArgumentParser()
parser.add_argument("name", help="name of output")
parser.add_argument("csv", help="csv file for varga")
parser.add_argument("tags", help="audacity label file")
args = parser.parse_args()


with open(args.csv) as csvfile:
    rows_csvfile = csv.DictReader(csvfile, delimiter=',', fieldnames=['sloka', 'line', 'text'])

    with open(args.tags) as tagsfile:
        rows_tagsfile = csv.DictReader(tagsfile, delimiter='\t', fieldnames=['time', 'label'])

        for c_i, t_i in zip(rows_csvfile, rows_tagsfile):
            print("%s,%s,%s,%s" % (args.name, c_i['sloka'], c_i['line'], t_i['time']))

# num_rows = min(len(rows_csvfile), len(rows_tagsfile))
#
# for i in range(0, num_rows):
#     print("%s,%s" % (rows_csvfile[i]['line'], rows_tagsfile[i][time]))
