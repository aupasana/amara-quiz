from flask import Flask, render_template, request, current_app, g
import random
import sqlite3 as sql

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

    term = request.args.get('term')

    try:
        with sql.connect('amara.db') as con:
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from pada inner join slokas on pada.sloka_number = slokas.sloka_number where pada = '%s' limit 25;" % term)
            rows = cur.fetchall();

            return render_template('search.html', rows=rows, term=term)
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
