from flask import Flask, render_template, request, current_app, g
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

import random
import sqlite3 as sql
import re

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')

def index():
    all_vargas = ['स्वर्गवर्गः','व्योमवर्गः','दिग्वर्गः','कालवर्गः','धीवर्गः','शब्दादिवर्गः','नाट्यवर्गः','पातालभोगिवर्गः','नरकवर्गः','वारिवर्गः','भूमिवर्गः','पुरवर्गः','शैलवर्गः','वनौषधिवर्गः','सिंहादिवर्गः','मनुष्यवर्गः','ब्रह्मवर्गः','क्षत्रियवर्गः','वैश्यवर्गः','शूद्रवर्गः','विशेष्यनिघ्नवर्गः','सङ्कीर्णवर्गः','विशेष्यनिघ्नवर्गः','सङ्कीर्णवर्गः','नानार्थवर्गः','अव्ययवर्गः']
    return render_template('index.html', all_vargas=all_vargas)

    # try:
    #     with sql.connect('amara.db') as con:
    #         con.row_factory = sql.Row
    #         cur = con.cursor()
    #         cur.execute("select distinct varga from pada")
    #         all_vargas = cur.fetchall();
    #         return render_template('index.html', all_vargas=all_vargas)
    # finally:
    #     con.close()

@app.route('/search')
def search():

    limit = 10
    offset = 0

    user_term = request.args.get('term')
    page = request.args.get('page')
    term = user_term

    if not page:
        page = 1

    offset = limit*(int(page) - 1)

    transliterate_regex = re.compile('.*[a-zA-Z].*')
    if (transliterate_regex.match(term)):
        term = transliterate(term, sanscript.ITRANS, sanscript.DEVANAGARI)

    term = term.replace("*", "%")
    term_words = term.split()

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            if len(term_words) == 1:
                cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada like ? or artha like ? order by id limit ? offset ?;", [term, term, limit, offset])
                rows = cur.fetchall();
            else:
                query = "select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada in (%s) order by pada limit 100;" % ','.join('?' for i in term_words)
                rows = cur.execute(query, term_words)

            return render_template('search.html', rows=rows, user_term=user_term, term=term, page=page)
    finally:
        con.close()


@app.route('/sloka')
def sloka():

    sloka_number = request.args.get('sloka_number')

    sloka_number_parts = sloka_number.split('.')

    sloka_number_previous = "%s.%s.%d" % (sloka_number_parts[0], sloka_number_parts[1], int(sloka_number_parts[2])-1)
    sloka_number_next = "%s.%s.%d" % (sloka_number_parts[0], sloka_number_parts[1], int(sloka_number_parts[2])+1)

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from mula where sloka_number = ? order by sloka_line;", [sloka_number])
            mula = cur.fetchall();

            cur.execute("select * from pada where sloka_number = ? order by id;", [sloka_number])
            pada = cur.fetchall();

            varga = ""
            if len(pada) > 0:
                varga = pada[0]["varga"]

            return render_template('sloka.html', mula=mula, pada=pada, varga=varga, sloka_number=sloka_number, sloka_number_previous=sloka_number_previous, sloka_number_next=sloka_number_next)
    finally:
        con.close()

@app.route('/quiz')
def quiz():

    varga = request.args.get('varga')

    try:
        rows =[]

        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.varga = ? order by random() limit 1;", [varga])
            rows = cur.fetchall();

            artha = rows[0]["artha"];
            cur.execute("select pada from pada where varga = ? and artha = ? order by id", [varga, artha]);
            paryaya = cur.fetchall();

            return render_template('quiz.html', rows=rows, paryaya=paryaya, varga=varga)
    finally:
        con.close()

@app.route('/varga')
def varga():

    varga = request.args.get('varga')

    try:
        rows =[]

        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            cur.execute("select * from mula where varga = ?;", [varga])
            mula = cur.fetchall();

            cur.execute("select sloka_line, artha, count(artha) artha_count, artha_english from pada where varga = ? group by sloka_line, artha, artha_english order by id;", [varga])
            artha_rows = cur.fetchall();

            artha_summary = {}

            for row in artha_rows:
                sloka_line = row["sloka_line"]

                if sloka_line not in artha_summary:
                    artha_summary[sloka_line] = ""

                if row["artha_english"]:
                    artha_summary[sloka_line] += " %s" % ( row["artha_english"] )
                artha_summary[sloka_line] += " %s (%d)." % ( row["artha"], row["artha_count"] )

            return render_template('varga.html', mula=mula, varga=varga, artha_summary=artha_summary)
    finally:
        con.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
