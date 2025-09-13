# save this as app.py
from passaBola import app,cpf_api_key
from flask import render_template, flash, redirect, url_for
from passaBola.forms import PlayerForm, TeamForm
from passaBola.models import Player, Teams
from passaBola.brasilApi import getBrazilStates

@app.route("/", methods=["GET", "POST"])
@app.route("/event", methods=["GET", "POST"])
def event_page():
    form = PlayerForm()
    teamForm = TeamForm()
    states = getBrazilStates()
    if form.validate_on_submit():
      #  print(cpf_api_key)
        newPlayer = Player( cpf=form.cpf.data, 
                            birthday=form.birthday.data,
                            full_name=form.full_name.data,
                            email=form.email.data,
                            phone=form.phone.data,
                            instagram=form.instagram.data)
        newPlayer.witeNewPlayer()
        return redirect(url_for("complete_page"))
          
  #  if teamForm.validate_on_submit():
  #      pass
    

    # Se não tiver erros nas validações => O próprio website já verifica somente de colocar as validações nos inputs
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'Ocorreu um erro durante a inscrição: {error}', category='danger')

    return render_template("event.html", form=form, teamForm=teamForm, brStates=states)


@app.route('/complete')
def complete_page():
    return render_template("complete.html")