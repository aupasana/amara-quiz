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
                cur.execute("select * from pada inner join slokas on pada.sloka_number = slokas.sloka_number where pada like '%s' or artha like '%s' order by id limit %d offset %d;" % (term, term, limit, offset))
                rows = cur.fetchall();
            else:
                query = "select * from pada inner join slokas on pada.sloka_number = slokas.sloka_number where pada in (%s) limit 100;" % ','.join('?' for i in term_words)
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
            cur.execute("select * from slokas left join pada on pada.sloka_number = slokas.sloka_number where slokas.sloka_number = '%s' order by id;" % sloka_number)
            rows = cur.fetchall();



            return render_template('sloka.html', rows=rows, sloka_number=sloka_number, varga=rows[0]["varga"], sloka_text=rows[0]["sloka_text"], sloka_number_previous=sloka_number_previous, sloka_number_next=sloka_number_next)
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
            cur.execute("select * from pada inner join slokas on pada.sloka_number = slokas.sloka_number where varga = '%s' order by random() limit 1;" % varga)
            rows = cur.fetchall();

            artha = rows[0]["artha"];
            cur.execute("select pada from pada where varga = '%s' and artha = '%s' order by id" % (varga, artha));
            paryaya = cur.fetchall();

            sloka_reference_parts = rows[0]["sloka_reference"].split('.')
            context_index = int(sloka_reference_parts[3]) - 1

            context_parts = rows[0]["sloka_text"].splitlines();
            context_parts[context_index] = '<span class="highlight">' + context_parts[context_index] + '</span>'

            context_html = "<br/>".join(context_parts)

            return render_template('quiz.html', rows=rows, paryaya=paryaya, varga=varga, context_html=context_html)
    finally:
        con.close()

    # context_index = int(sloka_index_line)-1
    # context[context_index] = '<span class="highlight">' + context[context_index] + '</span>'
    # context_html = "<br/>".join(context)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
