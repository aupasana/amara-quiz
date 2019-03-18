#!/usr/local/bin/python

import io, re

uid=1

with open('database/amara_pada.csv') as datafile:
    with open('database/tmp_pada.csv', 'w') as outputfile:

        while True:
            line = datafile.readline()
            if not line:
                break

            line = line.replace('_', ' ')
            parts = line.split(',')

          # The identifier in $fields[0] is a permanent unique id for coordinating
          # translations etc. We will generate a new identifier based on the file order
          # my $uid = $fields[0];

            pada_uid = parts[0]
            pada = parts[1]
            sloka_word = parts[2]
            linga = parts[3]
            varga = parts[4]
            artha = parts[5]

            re_parts = re.search (r'^([^.]+)\.([^.]+)\.([^.]+)\.([^.]+)\.([^.]+)', sloka_word);
            if re_parts:
                varga_number = "%s.%s" % (re_parts.group(1), re_parts.group(2))
                sloka_number = "%s.%s.%s" % (re_parts.group(1), re_parts.group(2), re_parts.group(3))
                sloka_line = "%s.%s.%s.%s" % (re_parts.group(1), re_parts.group(2), re_parts.group(3), re_parts.group(4))
            else:
                print ("Error with %s" % sloka_word)

            outputfile.write("%d,%s,%s,%s,%s,%s,%s,%s,%s,,,%s\n" % (uid, pada_uid, varga_number, sloka_number, sloka_line, sloka_word, pada, linga, varga, artha))
            uid = uid+1
