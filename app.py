from flask import Flask, render_template
from bs4 import BeautifulSoup
import random

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():

    lines = open('amara/amara_tokens_sb.utf8').read().splitlines()
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

    return render_template('index.html', question=question, varga=varga, answer=answer, sloka_index=sloka_index, sloka_number=sloka_number, context=context)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
