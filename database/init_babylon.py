#!/usr/local/bin/python

import io
import sys
import re
import sqlite3 as sql

def print_entry(cur, babylon_name, entry_number, head, subheads, body):

    if not head:
        return;

    cur.execute("insert into babylon (id, name, head, body) values (?, ?, ?, ?);", [entry_number, babylon_name, head, body])

    head_words = head.split("|")
    for head_word in head_words:
        stripped_head_word = head_word.strip('\n');
        cur.execute("insert into babylon_word (id, name, word) values (?, ?, ?);", [entry_number, babylon_name, stripped_head_word])

        for sub_word in subheads:
            stripped_sub_word = sub_word.strip('\n');
            if stripped_sub_word != "Comp.":                # compounds
                cur.execute("insert into babylon_word (id, name, word, sub_word) values (?, ?, ?, ?);", [entry_number, babylon_name, stripped_head_word, stripped_sub_word])

dicts = ["ap90.babylon" ];
# dicts = ["ap90.babylon", "vcp.babylon", "skd.babylon", "mw72.babylon"];

for dict in dicts:
    f = io.open("database/babylon/%s" % dict, mode="r", encoding="utf-8")
    entry_number = 1;
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

                match = re.compile(ur"--([^0-9][^ \),]*)", re.UNICODE)
                matches = match.findall(line);
                subheads = subheads + matches;
