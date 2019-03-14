# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, request, current_app, g, make_response
from flask_bootstrap import Bootstrap
from indic_transliteration import sanscript, xsanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

import random
import sqlite3 as sql
import re

app = Flask(__name__, static_url_path='', static_folder='static')
output_scripts = { 'telugu': xsanscript.TELUGU, 'kannada': xsanscript.KANNADA, 'malayalam': xsanscript.MALAYALAM, 'tamil': xsanscript.TAMIL }

mula_columns_all = [ 'id', 'varga_number', 'sloka_number', 'sloka_line', 'varga', 'sloka_text']
pada_columns_all = [ 'id', 'varga_number', 'sloka_number', 'sloka_line', 'sloka_word', 'pada', 'linga', 'varga', 'artha_english', 'artha']

columns_transliterate = {
    'pada': 'pada_transliterated',
    'linga': 'linga_transliterated',
    'varga': 'varga_transliterated',
    'sloka_text': 'sloka_text_transliterated',
    'artha': 'artha_transliterated'
}

def transliterate_term(output_script, term):
    if not output_script in output_scripts:
        return term
    else:
        xsanscript_script = output_scripts[output_script]
        return transliterate(term, xsanscript.DEVANAGARI, xsanscript_script)

def transliterate_factory(xsanscript_script, cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        column_name = col[0]
        d[column_name] = row[idx]

        if column_name in columns_transliterate:
            if xsanscript_script:
                d[columns_transliterate[column_name]] = transliterate(row[idx], xsanscript.DEVANAGARI, xsanscript_script)
            else:
                d[columns_transliterate[column_name]] = row[idx]
    return d

def transliterate_factory_script(language):
    xsanscript_script = None
    if language in output_scripts:
        xsanscript_script = output_scripts[language]

    def t(cursor, row):
        return transliterate_factory(xsanscript_script, cursor, row)
    return t

Bootstrap(app)

@app.route('/')
def index():
    all_vargas = ['स्वर्गवर्गः','व्योमवर्गः','दिग्वर्गः','कालवर्गः','धीवर्गः','शब्दादिवर्गः','नाट्यवर्गः','पातालभोगिवर्गः','नरकवर्गः','वारिवर्गः','भूमिवर्गः','पुरवर्गः','शैलवर्गः','वनौषधिवर्गः','सिंहादिवर्गः','मनुष्यवर्गः','ब्रह्मवर्गः','क्षत्रियवर्गः','वैश्यवर्गः','शूद्रवर्गः','विशेष्यनिघ्नवर्गः','सङ्कीर्णवर्गः','नानार्थवर्गः','अव्ययवर्गः']
    all_languages = ['devanagari', 'telugu', 'kannada', 'malayalam', 'tamil']

    language = request.args.get('language')
    if not language:
        language = request.cookies.get('amara_language')
    if not language:
        language = "devanagari"

    all_vargas_map = []
    for v in all_vargas:
        all_vargas_map.append({'varga': v, 'varga_transliterated': transliterate_term(language, v)})

    response = make_response(render_template('index.html', all_vargas_map=all_vargas_map, language=language, all_languages=all_languages))
    if language:
        response.set_cookie('amara_language', language)
    return response

@app.route('/index_babylon')
def index_babylon():
    return render_template('index_babylon.html')

@app.route('/search')
def search():

    limit = 10
    offset = 0

    user_term = request.args.get('term')
    page = request.args.get('page')
    language = request.cookies.get('amara_language')
    term = user_term

    if not page:
        page = 1

    offset = limit*(int(page) - 1)

    transliterate_regex = re.compile('.*[a-zA-Z].*')
    if (transliterate_regex.match(term)):
        term = transliterate(term, sanscript.ITRANS, sanscript.DEVANAGARI)

    term = term.replace("*", "%")
    user_term = user_term.replace("*", "%")
    term_words = term.split()

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
            cur = con.cursor()

            if len(term_words) == 1:
                cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada like ? or artha like ? or artha_english like ? order by id limit ? offset ?;", [term, term, user_term, limit, offset])
                rows = cur.fetchall();
            else:
                query = "select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada in (%s) order by pada limit 100;" % ','.join('?' for i in term_words)
                rows = cur.execute(query, term_words)

            resx = { 'artha': transliterate_term(language, 'अर्थः')}
            return render_template('search.html', rows=rows, user_term=user_term, term=term, page=page, resx=resx)
    finally:
        con.close()

@app.route('/babylon')
def babylon():

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
    user_term = user_term.replace("*", "%")

    sub_words = [];
    sub_words_delimiters = ["--", '-', '\\', '/'];
    for d in sub_words_delimiters:
        s = term.split(d)
        if len(s) > 1:
            sub_words = s;
            # print(sub_words);
            break;

    if len(sub_words) > 0:
        term = sub_words[0];
        sub_words.pop(0)

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            highlight_word = term.strip('%');
            highlight_sub_word = "";

            if len(sub_words) > 0:
                cur.execute("select distinct b.id, b.name, b.head, b.body from babylon b inner join babylon_word w on b.id = w.id and b.name = w.name where word like ? and sub_word like ? order by b.id limit ? offset ?;",
                                [term, sub_words[0], limit, offset])
                highlight_sub_word = sub_words[0].strip('%')
                # print("%s and %s" % (term, sub_words[0]));
            else:
                cur.execute("select distinct b.id, b.name, b.head, b.body from babylon b inner join babylon_word w on b.id = w.id and b.name = w.name where word like ? order by b.id limit ? offset ?;",
                [term, limit, offset])

            rows = cur.fetchall();


            return render_template('babylon.html', rows=rows, user_term=user_term, term=term, page=page, highlight_word=highlight_word, highlight_sub_word=highlight_sub_word)
    finally:
        con.close()


@app.route('/sloka')
def sloka():

    sloka_number = request.args.get('sloka_number')
    language = request.cookies.get('amara_language')

    sloka_number_parts = sloka_number.split('.')

    sloka_number_previous = "%s.%s.%d" % (sloka_number_parts[0], sloka_number_parts[1], int(sloka_number_parts[2])-1)
    sloka_number_next = "%s.%s.%d" % (sloka_number_parts[0], sloka_number_parts[1], int(sloka_number_parts[2])+1)

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
            cur = con.cursor()
            cur.execute("select * from mula where sloka_number = ? order by sloka_line;", [sloka_number])
            mula = cur.fetchall();

            cur.execute("select * from pada where sloka_number = ? order by id;", [sloka_number])
            pada = cur.fetchall();

            varga = ""
            if len(mula) > 0:
                varga = mula[0]["varga"]

            return render_template('sloka.html',
                mula=mula,
                pada=pada,
                varga=varga,
                varga_transliterated = transliterate_term(language, varga),
                sloka_number=sloka_number,
                sloka_number_previous=sloka_number_previous,
                sloka_number_next=sloka_number_next)
    finally:
        con.close()

@app.route('/quiz')
def quiz():

    varga = request.args.get('varga')
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        rows =[]

        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            if start and end:
                cur.execute("select id from pada where sloka_number = ? order by id limit 1;", [start])
                id_start = cur.fetchone()[0]

                cur.execute("select id from pada where sloka_number = ? order by id desc limit 1;", [end])
                id_end = cur.fetchone()[0]

                cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.id >= ? and pada.id <= ? order by random() limit 1;", [id_start, id_end])
                rows = cur.fetchall();
            else:
                cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.varga = ? order by random() limit 1;", [varga])
                rows = cur.fetchall();

            artha = rows[0]["artha"];
            varga = rows[0]["varga"];
            cur.execute("select pada from pada where varga = ? and artha = ? order by id", [varga, artha]);
            paryaya = cur.fetchall();

            if start and end:
                varga = "%s - %s" % (start, end)

            return render_template('quiz.html', rows=rows, paryaya=paryaya, varga=varga)
    finally:
        con.close()

@app.route('/pada')
def pada():

    pada = request.args.get('pada')
    number = request.args.get('pada_number')
    language = request.cookies.get('amara_language')

    try:
        rows =[]

        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
            cur = con.cursor()
            cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.sloka_word = ? and pada.pada = ?;", [number, pada])
            pada = cur.fetchall();

            artha = pada[0]["artha"];
            varga = pada[0]["varga"];

            cur.execute("select distinct mula.sloka_line, mula.sloka_number, mula.sloka_text, mula.varga from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.varga = ? and pada.artha = ? order by mula.sloka_line", [varga, artha]);
            paryaya_slokas=cur.fetchall();

            cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.varga = ? and pada.artha = ? order by pada.id", [varga, artha]);
            paryaya = cur.fetchall();

            resx = {"paryaya": transliterate_term(language, "पर्यायपदानि")}
            return render_template('pada.html',
                pada=pada,
                paryaya=paryaya,
                paryaya_slokas=paryaya_slokas,
                varga=varga,
                resx=resx)
    finally:
        con.close()

@app.route('/varga')
def varga():

    varga = request.args.get('varga')
    sloka_number = request.args.get('sloka_number')
    language = request.cookies.get('amara_language')

    if (not varga) and sloka:
        try:
            with sql.connect('amara.db') as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                cur.execute("select varga from mula where sloka_number = ? limit 1;", [sloka_number])
                mula = cur.fetchall();

                return redirect("/varga?varga=%s#%s" % (mula[0]["varga"], sloka_number))
        finally:
            con.close()


    try:
        rows =[]

        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
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

@app.route('/all_pada')
def all_pada():
    prefixes = [
        [ 'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ए', 'ऐ', 'ओ', 'औ' ],
        [ 'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ' ],
        [ 'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न' ],
        [ 'प', 'फ', 'ब', 'भ', 'म' ],
        [ 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह' ] ]
    padas = []

    prefix = request.args.get('prefix')

    if prefix:
        try:
            with sql.connect('amara.db') as con:
                con.row_factory = sql.Row
                cur = con.cursor()

                cur.execute("select distinct pada, sloka_word from pada where pada like ? order by pada, id;", ["%s%%" % prefix])
                padas = cur.fetchall()

                return render_template('all_pada.html', prefixes=prefixes, padas=padas, prefix=prefix)

        finally:
            con.close()
    else:
        return render_template('all_pada.html', prefixes=prefixes, padas=[], prefix=prefix)

@app.route('/dupe_pada')
def dupe_pada():
    try:
        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            # cur.execute("select pada, count(*) c from pada group by pada having count(*) > 1 order by pada;")
            cur.execute("""
                            select c.cnt occurences, p.pada, p.artha, p.sloka_word from
                            (select pada, count(*) cnt from pada group by pada) c
                            inner join pada p on c.pada = p.pada
                            where c.cnt > 1
                            order by p.pada; """)

            padas = cur.fetchall()

            return render_template('dupe_pada.html', padas=padas)

    finally:
        con.close()


@app.route('/stats')
def stats():
    try:
        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            # cur.execute("select pada, count(*) c from pada group by pada having count(*) > 1 order by pada;")
            cur.execute("""
                            select m.varga, m.c mula_count, p.c pada_count from
                                (select varga, id, count(varga) c from mula group by varga) m
                            inner join
                                (select varga, id, count(varga) c from pada group by varga order by id) p
                            on m.varga = p.varga
                            order by m.id; """)

            stats = cur.fetchall()

            return render_template('stats.html', stats=stats)

    finally:
        con.close()

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
@app.errorhandler(500)
def error(error):
    return render_template('error.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
