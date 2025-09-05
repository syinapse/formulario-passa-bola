# save this as app.py
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def hello():
    url_for('static', filename='style.css')
    url_for('static', filename='script.js')
    return render_template("index.html")
