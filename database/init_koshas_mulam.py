#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import io
import sys
import re
import sqlite3 as sql
from indic_transliteration import sanscript, xsanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

from pathlib import Path

for fname in Path('database/kosha').glob('**/*.txt'):
    f = io.open(fname, mode="r", encoding="utf-8")

    fname_string = "%s" % fname
    fname_string = fname_string[len("database/kosha/"):]

    if re.match(".*scripts.*", fname_string):
        continue

    print ("")
    print (fname)
    line_number = 1

    with sql.connect('database/koshas_mulam.db') as con:
        con.row_factory = sql.Row
        cur = con.cursor()

        for line in f:
            line_stripped = line.strip('\n')

            if re.match(r'^\uFEFF*;', line_stripped):
                continue
            else:
                line_slp1 = transliterate(line_stripped, xsanscript.DEVANAGARI, xsanscript.SLP1)

                cur.execute("insert into koshas_mulam_line (kosha_name, line_id, text_slp1, text_line) values (?, ?, ?, ?);", [fname_string, line_number, line_slp1, line_stripped])

                # print ("%s,%d,%s,%s" % (fname, line_number, line_slp1, line_stripped) )
                # print (fname, line_number, line_slp1)
                print('.', end='')

                line_number = line_number + 1

