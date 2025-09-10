# save this as app.py
from passaBola import app
from flask import render_template, url_for
@app.route("/")
def hello():
    url_for('static', filename='style.css')
    url_for('static', filename='script.js')
    return render_template("index.html")
