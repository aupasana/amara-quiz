#!/usr/local/bin/python

import io
import sys
import re
import sqlite3 as sql


def print_entry(cur, babylon_name, entry_number, head, body):
    # print "%s%s%s" % (entry_number, head, body)
    cur.execute("insert into babylon (id, name, head, body) values (?, ?, ?, ?);", [entry_number, babylon_name, head, body])

    head_words = head.split("|")
    for head_word in head_words:
        cur.execute("insert into babylon_word (id, name, word) values (?, ?, ?);", [entry_number, babylon_name, head_word.strip('\n')])

        # sys.stdout.write ("head_word is %s\n" % head_word.strip('\n'))


    # sys.stdout.write ("parsed entry for %s" % head.encode('utf-8'))
    # sys.stdout.write ("body is %s" % body)


f = io.open("database/babylon/ap90.babylon", mode="r", encoding="utf-8")
entry_number = 1;
babylon_name = "apte";

head = None;
body = "";

with sql.connect('docker/amara.db') as con:
    con.row_factory = sql.Row
    cur = con.cursor()

    for line in f:
        if re.match(r'^$', line):
            print_entry(cur, babylon_name, entry_number, head, body);

            head = None;
            body="";
            entry_number = entry_number + 1;
            continue;

        if head == None:
            head = line;
        else:
            body = "%s\n\n%s" % (body, line)
