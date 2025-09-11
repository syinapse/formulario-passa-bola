# save this as app.py
from passaBola import app
from flask import render_template
from passaBola.forms import PlayerForm, TeamForm


@app.route("/", methods=["GET", "POST"])
@app.route("/event")
def event_page():
    form = PlayerForm()
    teamForm = TeamForm()
    if form.validate_on_submit():
        pass
    return render_template("event.html", form=[form, teamForm])
