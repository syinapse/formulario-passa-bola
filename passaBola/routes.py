# save this as app.py
from passaBola import app,cpf_api_key
from flask import render_template, flash, redirect, url_for
from passaBola.forms import PlayerForm, TeamForm
from passaBola.models import Player, Teams
from passaBola.brasilApi import getBrazilStates

@app.route("/", methods=["GET", "POST"])
@app.route("/event", methods=["GET", "POST"])
def event_page():
    form = PlayerForm(city="")
    teamForm = TeamForm(teamCity="")
    if form.validate_on_submit():
      #  print(cpf_api_key)
        newPlayer = Player( cpf=form.cpf.data, 
                            birthday=form.birthday.data,
                            full_name=form.full_name.data,
                            city = form.city.data,
                            email=form.email.data.lower(),
                            phone=form.phone.data,
                            instagram=form.instagram.data)
        newPlayer.witeNewPlayer()
        for k in form.data.keys():
            form.data[k] = ""
        return redirect(url_for("complete_page"))
          
    if teamForm.validate_on_submit():
        newTeam = Teams(cnpj=teamForm.cnpj.data,
                        team_name=teamForm.team_name.data,
                        president_name=teamForm.president_name.data,
                        email=teamForm.teamEmail.data.lower(),
                        city=teamForm.teamCity.data,
                        phone=teamForm.teamPhone.data)
        
        playersList = []
        temp = teamForm.players.data.strip().splitlines()
        for pl in temp:
            split = pl.split('-')
            newPlayer = Player.TeamsPlayers(cpf=split[1].strip(), name=split[0].strip())
            # Adicionando a lista de jogadoras formatadas
            playersList.append(newPlayer)
        newTeam.players = playersList
        newTeam.writeTeams()
     #   for k in teamForm.data.keys():
     #       form.data[k] = ""
        return redirect(url_for("complete_page"))


    # Se não tiver erros nas validações => O próprio website já verifica somente de colocar as validações nos inputs
    
    if form.cpf.data:
      if form.errors != {}:
        for errors in form.errors.values():
            for e in errors:
              flash(f'{e}', category='danger')
    elif teamForm.cnpj.data:
      if teamForm.errors != {}:
        for errors in teamForm.errors.values():
            for e in errors:
              flash(f'{e}', category='danger')

    return render_template("event.html", form=form, teamForm=teamForm)


@app.route('/complete')
def complete_page():
    return render_template("complete.html")