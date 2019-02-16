from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import random

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    # all_vargas = ['स्वर्गवर्गः', 'व्योमवर्गः', 'दिग्वर्गः', 'कालवर्गः', 'धीवर्गः']
    all_vargas = ['स्वर्गवर्गः','व्योमवर्गः','दिग्वर्गः','कालवर्गः','धीवर्गः','शब्दादिवर्गः','नाट्यवर्गः','पातालभोगिवर्गः','नरकवर्गः','वारिवर्गः','भूमिवर्गः','पुरवर्गः','शैलवर्गः','वनौषधिवर्गः','सिंहादिवर्गः','मनुष्यवर्गः','ब्रह्मवर्गः','क्षत्रियवर्गः','वैश्यवर्गः','शूद्रवर्गः','विशेष्यनिघ्नवर्गः','सङ्कीर्णवर्गः','विशेष्यनिघ्नवर्गः','सङ्कीर्णवर्गः','नानार्थवर्गः','अव्ययवर्गः']
    return render_template('index.html', all_vargas=all_vargas)

@app.route('/quiz')
def quiz():

    filter = request.args.get('varga')
    filename = 'amara/tokens_' + filter + '.utf8'
    # filename = secure_filename(filename)
    lines = open(filename).read().splitlines()

    question_line = random.choice(lines)
    question_line_parts = question_line.split(",")

    question = question_line_parts[0]
    sloka_index = question_line_parts[1]
    varga = question_line_parts[3]
    sloka_index_parts = sloka_index.split(".")
    sloka_index_relevant_parts = sloka_index_parts[0:3]
    sloka_number = ".".join(sloka_index_relevant_parts)
    answer = question_line_parts[4]
    answer = answer.replace("_", " ")

    mulam_html = open('static/amara_mulam.html')
    soup = BeautifulSoup(mulam_html, 'html.parser')

    context = soup.findAll('div', attrs={'id' : sloka_number})[0]

    return render_template('quiz.html', question=question, varga=varga, answer=answer, sloka_index=sloka_index, sloka_number=sloka_number, context=context, filter=filter)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
