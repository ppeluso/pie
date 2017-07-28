from flask import Flask, render_template
import os
import geojson
import geo
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object('config')

class ReviewForm(FlaskForm):
    name = StringField('name')
    search_info = StringField("Info")
    score = FloatField("sore")


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/json_file')
def json_file():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    js = 'eqfeed_callback({"type\": "FeatureCollection","features": ['
    for row in c.execute('SELECT * FROM reviews'):
        loc = geo.ReviewGeoJSON(row[0],row[1], row[2], row[3])
        js = js+ geojson.dumps(loc) + ','
    js = js + " ]});"
    return js
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = ReviewForm()
    if form.validate_on_submit():
        loc = geo.Review(form.data["name"], form.data["search_info"], form.data["score"])
        loc.to_sql()
    return render_template('submitreview.html', 
                           form=form)
if __name__ == '__main__':
    app.run()
