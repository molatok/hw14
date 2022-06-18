from flask import Flask, render_template, jsonify
from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return '''index'''


@app.route('/movie/<title>')
def get_name_movie(title):
    return film_by_title(title)

@app.route('/movie/<int:years_start>-<int:years_end>')
def get_film_by_release(years_start, years_end):
    return jsonify(film_by_release(years_start, years_end))

@app.route('/rating/<rating_group>')
def get_film_by_rating(rating_group):
    return jsonify(film_by_rating(rating_group))

@app.route('/genre/<genre>')
def get_film_by_genre(genre):
    return jsonify(film_by_genre(genre))

if __name__ == "__main__":
    app.run()
