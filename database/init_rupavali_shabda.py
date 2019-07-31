#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import io
import sys
import re
import sqlite3 as sql
from indic_transliteration import sanscript, xsanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

from pathlib import Path

f = io.open("database/rupavali/nsp-shabda-rupavali.txt", mode="r", encoding="utf-8")

rupavali_number = 0
line_count = 0
rupavali = ""

with sql.connect('database/rupavali_shabda.db') as con:
    con.row_factory = sql.Row
    cur = con.cursor()

    for line in f:
        line_stripped = line.strip('\n')
        
        if len(line_stripped) == 0:
            continue

        if line_stripped[0] == '#':

            if line_count > 1:
                ending_slp1 = transliterate(ending, xsanscript.ITRANS, xsanscript.SLP1)
                ending_last_slp1 = ending_slp1[len(ending_slp1)-1]
                ending_last = transliterate(ending_last_slp1, xsanscript.SLP1, xsanscript.DEVANAGARI)
                cur.execute("insert into rupavali_shabda (id, anta, anta_slp1, anta_last, anta_last_slp1, linga, pratipadika, category, rupavali) values (?, ?, ?, ?, ?, ?, ?, ?, ?);", 
                [rupavali_number, ending, ending_slp1, ending_last, ending_last_slp1, linga, pada, category, rupavali])

                line_count = 0
                rupavali = ""

            rupavali_number = rupavali_number + 1

            re_parts_three = re.search (r'^# ([^,]*),([^,]*),([^,]*),{0,1}([^,]*)$', line_stripped)
            if re_parts_three:
                ending = re_parts_three[1]
                linga = re_parts_three[2]
                pada = re_parts_three[3]
                category = re_parts_three[4]

                if category == "":
                    category = "shabda"
                if category == "s":
                    category = "sarvanAma"
                if category == "sankhya":
                    category = "sa~NkhyA"

            else:
                print ("Warning: no match for", line_stripped)
                
        else:
            line_count = line_count + 1
            rupavali = rupavali + line






