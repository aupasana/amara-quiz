# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, request, current_app, g, make_response
from flask_bootstrap import Bootstrap
from indic_transliteration import detect, sanscript, xsanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

import random
import sqlite3 as sql
import re

app = Flask(__name__, static_url_path='', static_folder='static')
output_scripts = { 'telugu': xsanscript.TELUGU, 'kannada': xsanscript.KANNADA, 'malayalam': xsanscript.MALAYALAM, 'tamil': xsanscript.TAMIL, 'iast': xsanscript.IAST }

columns_transliterate = {
    'varga': 'varga_transliterated',
    'pada': 'pada_transliterated',
    'linga': 'linga_transliterated',
    'varga': 'varga_transliterated',
    'sloka_text': 'sloka_text_transliterated',
    'artha': 'artha_transliterated',
    'pada_group': 'pada_group_transliterated'
}

class HighlightIncrementReplace:
    def __init__(self):
        self.count = 1
    def replace(self, matchObject):
        ret =  '<span class="highlight" id="match-%d">%s</span>' % (self.count, matchObject.group(1))
        self.count += 1
        return ret;

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
    all_languages = ['devanagari', 'iast', 'telugu', 'kannada', 'malayalam', 'tamil']

    language = request.args.get('language')
    if not language:
        language = request.cookies.get('amara_language')
    if not language:
        language = "devanagari"

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
            cur = con.cursor()

            cur.execute("select * from varga order by id;")
            vargas = cur.fetchall();
    finally:
        con.close()

    response = make_response(render_template('index.html', all_vargas_map=vargas, language=language, all_languages=all_languages))
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
    search_box_value = request.args.get('term')
    page = request.args.get('page')
    language = request.cookies.get('amara_language')
    term = user_term

    if not page:
        page = 1

    offset = limit*(int(page) - 1)

    term_script = detect.detect(term).lower()
    term = transliterate(term, term_script, xsanscript.SLP1)

    # transliterate_regex = re.compile('.*[a-zA-Z].*')
    # if (transliterate_regex.match(term)):
    #     term = transliterate(term, sanscript.ITRANS, sanscript.DEVANAGARI)

    term = term.replace("*", "%")
    user_term = user_term.replace("*", "%")
    term_words = term.split()

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
            cur = con.cursor()
            cur.execute('PRAGMA case_sensitive_like = ON')

            search_converted = None

            if len(term_words) == 1:
                cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada_slp1 like ? or artha like ? or artha_english like ? order by id limit ? offset ?;", [term, term, user_term, limit, offset])
                rows = cur.fetchall();

                if len(rows) == 0 and offset == 0 and (not term[-1:] == '%'):
                    search_converted = "No results found for %s. Converting to prefix search %s" % (term, term + "%")
                    term = term + "%"
                    user_term = user_term + "%"

                    cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada_slp1 like ? or artha like ? or artha_english like ? order by id limit ? offset ?;", [term, term, user_term, limit, offset])
                    rows = cur.fetchall();

            else:
                query = "select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada_slp1 in (%s) order by pada limit 100;" % ','.join('?' for i in term_words)
                rows = cur.execute(query, term_words)

            resx = { 'artha': transliterate_term(language, 'अर्थः')}
            return render_template('search.html', rows=rows, user_term=user_term, term=term, page=page, search_converted=search_converted, resx=resx, search_box_value=search_box_value)
    finally:
        con.close()

@app.route('/babylon')
def babylon():

    limit = 10
    offset = 0

    user_term = request.args.get('term')
    search_box_value = request.args.get('term')
    page = request.args.get('page')
    term = user_term

    if not page:
        page = 1

    offset = limit*(int(page) - 1)

    term_script = detect.detect(term).lower()
    term = transliterate(term, term_script, xsanscript.SLP1)

    # transliterate_regex = re.compile('.*[a-zA-Z].*')
    # if (transliterate_regex.match(term)):
    #     term = transliterate(term, sanscript.ITRANS, sanscript.DEVANAGARI)

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

    context_summary = []

    try:
        with sql.connect('babylon.db') as con:
            con.row_factory = lambda C, R: { c[0]: R[i] for i, c in enumerate(C.description) }
            cur = con.cursor()
            cur.execute('PRAGMA case_sensitive_like = ON')

            highlight_word = term.strip('%');
            highlight_sub_word = "";

            if len(sub_words) > 0:
                cur.execute("select distinct b.id, b.name, b.head, b.body from babylon b inner join babylon_word w on b.id = w.id and b.name = w.name where word_slp1 like ? and sub_word_slp1 like ? order by b.id limit ? offset ?;",
                                [term, sub_words[0], limit, offset])
                highlight_sub_word = sub_words[0].strip('%')
                highlight_sub_word = transliterate(highlight_sub_word, xsanscript.SLP1, xsanscript.DEVANAGARI)

                # trim trailing virama
                if highlight_sub_word[-1:] == '्':
                    highlight_sub_word = highlight_sub_word[:-1]

                rows = cur.fetchall();
                rep = HighlightIncrementReplace()
                match_number = 1
                for r in rows:
                    for m in re.finditer(r'(--%s[^\r\n]*)' % highlight_sub_word, r["body"]):
                        context_summary.append({"number": match_number, "name": r["name"], "head": r["head"], "match": m.group(1)})
                        match_number += 1

                    r["body"] = re.sub(r'(--%s[^\r\n]*)' % highlight_sub_word, rep.replace, r["body"])

            else:
                cur.execute("select distinct b.id, b.name, b.head, b.body from babylon b inner join babylon_word w on b.id = w.id and b.name = w.name where word_slp1 like ? order by b.id limit ? offset ?;",
                [term, limit, offset])

                rows = cur.fetchall();


            return render_template('babylon.html', rows=rows, user_term=user_term, term=term, page=page, highlight_word=highlight_word, highlight_sub_word=highlight_sub_word, search_box_value=search_box_value, route='/babylon', context_summary=context_summary)
    finally:
        con.close()

@app.route('/babylon-english')
def babylon_english():

    limit = 10
    offset = 0

    term = request.args.get('term')
    page = request.args.get('page')

    if not page:
        page = 1

    offset = limit*(int(page) - 1)

    try:
        with sql.connect('babylon.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute('PRAGMA case_sensitive_like = OFF')

            cur.execute("select distinct b.id, b.name, b.head, b.body from babylon b where b.body like ? order by b.id limit ? offset ?;",
            [term, limit, offset])

            rows = cur.fetchall();

            return render_template('babylon.html', rows=rows, user_term=term, term=term, page=page, search_box_value=term, route='/babylon-english')
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

            cur.execute("select * from audio where sloka_number = ? order by sloka_line;", [sloka_number])
            audio = cur.fetchall();

            varga = ""
            if len(mula) > 0:
                varga = mula[0]["varga"]

            return render_template('sloka.html',
                audio=audio,
                mula=mula,
                pada=pada,
                varga=varga,
                varga_transliterated = transliterate_term(language, varga),
                language=language,
                sloka_number=sloka_number,
                sloka_number_previous=sloka_number_previous,
                sloka_number_next=sloka_number_next)
    finally:
        con.close()

def pada_quiz_common(quiz, cur, pada, padas, language):
    artha = padas[0]["artha"];
    varga = padas[0]["varga"];

    cur.execute("select distinct mula.sloka_line, mula.sloka_number, mula.sloka_text, mula.varga from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.varga = ? and pada.artha = ? order by mula.sloka_line", [varga, artha]);
    paryaya_slokas=cur.fetchall();

    cur.execute("select distinct mula.sloka_line, mula.sloka_number, mula.sloka_text, mula.varga from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.pada = ? and pada.artha != ? order by mula.sloka_line", [pada, artha]);
    not_paryaya_slokas=cur.fetchall();

    cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.varga = ? and pada.artha = ? order by pada.id", [varga, artha]);
    paryaya = cur.fetchall();

    cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.pada = ? and pada.artha != ? order by pada.id", [pada, artha]);
    not_paryaya = cur.fetchall();

    resx = {"paryaya": transliterate_term(language, "पर्यायपदानि"), "arthantaram": transliterate_term(language, "अर्थान्तरम्")}
    return render_template('pada.html',
        pada=padas,
        paryaya=paryaya,
        not_paryaya=not_paryaya,
        paryaya_slokas=paryaya_slokas,
        not_paryaya_slokas=not_paryaya_slokas,
        varga=varga,
        resx=resx,
        quiz=quiz)

@app.route('/quiz')
def quiz():

    varga = request.args.get('varga')
    start = request.args.get('start')
    end = request.args.get('end')
    pada = request.args.get('pada')
    number = request.args.get('pada_number')
    language = request.cookies.get('amara_language')

    try:
        rows =[]

        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
            cur = con.cursor()

            if start and end:
                cur.execute("select id from pada where sloka_number = ? order by id limit 1;", [start])
                id_start = cur.fetchone()[0]

                cur.execute("select id from pada where sloka_number = ? order by id desc limit 1;", [end])
                id_end = cur.fetchone()[0]

                cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.id >= ? and pada.id <= ? and is_variant = 0 order by random() limit 1;", [id_start, id_end])
            else:
                cur.execute("select * from pada inner join mula on pada.sloka_line = mula.sloka_line where pada.varga = ? and is_variant = 0 order by random() limit 1;", [varga])

            question_rows = cur.fetchall();

            return pada_quiz_common(True, cur, pada, question_rows, language)
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
            pada_rows = cur.fetchall();

            return pada_quiz_common(False, cur, pada, pada_rows, language)

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

            if language == 'telugu':
                artha_translation_column = 'artha_telugu'
            else:
                artha_translation_column = 'artha_english'

            cur.execute("""
                select sloka_line, artha, count(artha) artha_count, %s, group_concat(pada_linga, ", ") pada_group
                from (
                  select id, sloka_line, artha, %s,
                    case when is_variant = 0
                        then pada || " (" || linga || ")"
                        else "+[" || pada || " (" || linga || ")]"
                    end pada_linga
                  from pada
                  where varga = ?
                ) group by sloka_line, artha order by id;""" % (artha_translation_column, artha_translation_column), [varga])
            artha_rows = cur.fetchall();

            artha_summary = {}

            for row in artha_rows:
                sloka_line = row["sloka_line"]
                if sloka_line not in artha_summary:
                    artha_summary[sloka_line] = []
                    summaries = []

                summary = "%s. %s (%d) - %s " % ( row["artha_transliterated"], row[artha_translation_column], row["artha_count"], row["pada_group_transliterated"] )
                artha_summary[sloka_line].append(summary)

            return render_template('varga.html', mula=mula, varga=varga, varga_transliterated=transliterate_term(language,varga), artha_summary=artha_summary)
    finally:
        con.close()

@app.route('/all_pada')
def all_pada():
    prefix = request.args.get('prefix')
    language = request.cookies.get('amara_language')

    prefixes = [
        'अ आ इ ई उ ऊ ऋ ॠ ए ऐ ओ औ',
        'क ख ग घ ङ च छ ज झ ञ',
        'ट ठ ड ढ ण त थ द ध न',
        'प फ ब भ म',
        'य र ल व श ष स ह' ]
    padas = []

    prefixes_transliterated = []
    for row in prefixes:
        row_transliterated = []
        for l in row.split(' '):
            row_transliterated.append({"prefix": l, "prefix_transliterated" : transliterate_term(language, l)})
        prefixes_transliterated.append(row_transliterated)

    if prefix:
        try:
            with sql.connect('amara.db') as con:
                con.row_factory = transliterate_factory_script(language)
                cur = con.cursor()

                cur.execute("select distinct pada, is_variant, sloka_word from pada where pada like ? order by pada, id;", ["%s%%" % prefix])
                padas = cur.fetchall()

                return render_template('all_pada.html', prefixes=prefixes_transliterated, padas=padas, prefix=prefix)

        finally:
            con.close()
    else:
        return render_template('all_pada.html', prefixes=prefixes_transliterated, padas=[], prefix=prefix)

@app.route('/dupe_pada')
def dupe_pada():
    language = request.cookies.get('amara_language')
    try:
        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
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
    language = request.cookies.get('amara_language')

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = transliterate_factory_script(language)
            cur = con.cursor()

            # cur.execute("select pada, count(*) c from pada group by pada having count(*) > 1 order by pada;")
            cur.execute("""
                            select k.kanda, m.varga, m.c mula_count, p.c pada_count, coalesce(v.c, 0) variant_count from
                                (select varga, id, count(varga) c from mula group by varga) m
                            inner join
                                (select varga, id, count(varga) c from pada where is_variant = 0 group by varga order by id) p
                                on m.varga = p.varga
                            inner join varga k on m.varga = k.varga
                            left join
                                (select varga, id, count(varga) c from pada where is_variant = 1 group by varga order by id) v
                                on m.varga = v.varga
                            order by m.id; """)

            stats = cur.fetchall()

            return render_template('stats.html', stats=stats)

    finally:
        con.close()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.errorhandler(404)
@app.errorhandler(500)
def error(error):
    return render_template('error.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
