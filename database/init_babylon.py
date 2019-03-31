#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import io
import sys
import re
import sqlite3 as sql
from indic_transliteration import sanscript, xsanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

entry_number = 1;

def print_entry(cur, babylon_name, entry_number, head, subheads, body):

    if not head:
        return;

    cur.execute("insert into babylon (id, name, head, body) values (?, ?, ?, ?);", [entry_number, babylon_name, head, body])

    head_words = head.split("|")
    for head_word in head_words:
        stripped_head_word = head_word.strip('\n');
        word_slp1 = transliterate(stripped_head_word, xsanscript.DEVANAGARI, xsanscript.SLP1)

        cur.execute("insert into babylon_word (id, name, word, word_slp1) values (?, ?, ?, ?);", [entry_number, babylon_name, stripped_head_word, word_slp1])

        for sub_word in subheads:
            stripped_sub_word = sub_word.strip('\n');
            if stripped_sub_word != "Comp.":                # compounds
                sub_word_slp1 = transliterate(stripped_sub_word, xsanscript.DEVANAGARI, xsanscript.SLP1)
                cur.execute("insert into babylon_word (id, name, word, word_slp1, sub_word, sub_word_slp1) values (?, ?, ?, ?, ?, ?);", [entry_number, babylon_name, stripped_head_word, word_slp1, stripped_sub_word, sub_word_slp1])

# dicts = ["ap90.babylon" ];
dicts = ["ap90.babylon", "vcp.babylon", "skd.babylon", "mw72.babylon"];

for dict in dicts:
    f = io.open("database/babylon/%s" % dict, mode="r", encoding="utf-8")
    babylon_name = dict

    head = None;
    body = "";
    subheads = [];

    with sql.connect('database/babylon.db') as con:
        con.row_factory = sql.Row
        cur = con.cursor()

        for line in f:
            if re.match(r'^$', line):
                print_entry(cur, babylon_name, entry_number, head, subheads, body);

                head = None;
                body="";
                subheads = [];

                entry_number = entry_number + 1;
                continue;

            if head == None:
                head = line;
            else:
                body = "%s\n\n%s" % (body, line)

                match = re.compile('--([^0-9][^ \),]*)')
                matches = match.findall(line);
                subheads = subheads + matches;
