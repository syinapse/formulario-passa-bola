# Importa as dependências necessárias do Flask e os módulos da aplicação.
# save this as app.py
from passaBola import app,cpf_api_key
from flask import render_template, flash, redirect, url_for, request
from passaBola.forms import PlayerForm, TeamForm, LoginForm, EventForm
from passaBola.models import Player, Teams, User, Events, Database
from passaBola.brasilApi import getBrazilStates, getStateByUf
from flask_login import login_user, logout_user, login_required
import os

# Define a rota para a página principal do formulário, aceitando métodos GET e POST.
@app.route("/login", methods=["GET", "POST"])
def login_page():
    loginform = LoginForm()

    if loginform.validate_on_submit():
      attemptedUser = User.findUserByEmail(loginform.email.data)

      if (attemptedUser and attemptedUser.isValidPassword(attempedPassword=loginform.password.data)):
          login_user(attemptedUser)
          flash("Acesso concedido!", category="success")
          return redirect(url_for('admin_page'))
      else:
          flash("Email ou senha estão incorretos... Tente novamente.", category="danger")
      
    return render_template("login.html", form=loginform)

# precisa obter o parametro como Id par pegar os dados como /event/id ou /event?id=id
@app.route("/")
@app.route("/home")
def home_page():
   return render_template('home.html')

@app.route('/home/events')
def home_events_page():
    all_users = Database.readDatabase(Database.db_profile)
    all_events = []
    for data in all_users.values():
        for event_id in data['events']:
            all_events.append(Events.findEventById(event_id))
    all_events_total = len(all_events)

    return render_template('home_events.html', all_events=all_events, all_events_total=all_events_total)

@app.route('/event')
@app.route("/event/<uuid:event_id>", methods=["GET", "POST"])
def event_page(event_id = None):
    if not event_id:
        flash(f'ERRO: Informe um ID antes de acessar os eventos', category='danger')
        return redirect(url_for('home_page'))

    event = Events.findEventById(str(event_id))
    event.state = getStateByUf(event.state)
    if not event:
        flash(f'Evento não encontrado. Acesse um evento existente', category='warning')
        return redirect(url_for('home_page'))

    form = PlayerForm(state="")
    teamForm = TeamForm(teamState="")

    formType = request.form.get('form_type')

    if formType == 'individuals':
      if form.validate_on_submit():
          newPlayer = Player( cpf=form.cpf.data, 
                              birthday=form.birthday.data,
                              full_name=form.full_name.data,
                              state=form.state.data,
                              email=form.email.data.lower(),
                              phone=form.phone.data,
                              instagram=form.instagram.data)
          newPlayer.writeNewPlayer(event.id)
          return redirect(url_for("complete_page"))
      
      if form.errors != {}:
          for errors in form.errors.values():
              for e in errors:
                flash(f'{e}', category='danger')  

    if formType == 'teams':    
      if teamForm.validate_on_submit():  
          newTeam = Teams(cnpj=teamForm.cnpj.data,
                          team_name=teamForm.team_name.data,
                          president_name=teamForm.president_name.data,
                          email=teamForm.teamEmail.data.lower(),
                          state=teamForm.teamState.data,
                          phone=teamForm.teamPhone.data)
          
          try:
            playersList = []
            temp = teamForm.players.data.strip().splitlines()
            for pl in temp:
                split = pl.split('-')
                newPlayer = Player.TeamsPlayers(cpf=split[1].strip(), name=split[0].strip())
                playersList.append(newPlayer)

            # Adiciona a lista de jogadoras ao objeto do time e salva no JSON.
            newTeam.players = playersList
            newTeam.writeTeams(event.id)
            return redirect(url_for("complete_page"))
          except Exception:
            flash("Ocorreu um erro enviar o formulário de Times. Confira os campos e tente novamente", category='danger')

      # Se houver erros de validação no formulário do time, exibe as mensagens.
      if teamForm.errors != {}:
        for errors in teamForm.errors.values():
            for e in errors:
              flash(f'{e}', category='danger')

    # Renderiza o template da página de eventos, passando os dois formulários para o HTML.
    return render_template("event.html", form=form, teamForm=teamForm, event=event)

# Define a rota para a página de conclusão/sucesso.
@app.route('/complete')
def complete_page():
    return render_template("complete.html")


@app.route('/admin', methods=['GET'])
@app.route('/admin/home', methods=['GET'])
@login_required
def admin_page():
   return render_template('adminPages/home.html')

@app.route('/admin/new-event', methods=['GET', 'POST'])
@login_required
def admin_newEvent_page():
    eventForm = EventForm()
    user_id = str(request.args.get('id'))

    if eventForm.validate_on_submit():
      try:
        if (eventForm.event_date_start.data > eventForm.event_date_end.data):
          raise ValueError("A data de inicio do evento não pode ser menor que a data de encerramento")

        newEvent = Events(
                title=eventForm.title.data,
                address=eventForm.address.data,
                state=eventForm.state.data,
                begin_date=eventForm.event_date_start.data,
                end_date=eventForm.event_date_end.data,
                event_description=eventForm.event_description.data,
                reward_description=eventForm.event_reward.data,
                min_age=eventForm.min_age.data,
                max_age=eventForm.max_age.data,
                max_uni_sub=eventForm.max_total_uni.data,
                max_team_sub=eventForm.max_total_team.data,
                cost_team_sub=eventForm.cost_team.data,
                cost_uni_sub=eventForm.cost_uni.data,
                linkedin=eventForm.linkedin_link.data,
                instagram=eventForm.instagram_link.data,
                whats=eventForm.whatsapp_link.data
            ) 
        newEvent.writeNewEvent(user_id)
        flash("O novo evento foi criado com sucesso!", category='success')

      except Exception as e:
        flash(f'{e}', category='danger')

    if eventForm.errors != {}:
      for errors in eventForm.errors.values():
        for e in errors:
          flash(f'{e}', category='danger')
    
    return render_template('adminPages/writeEvent.html', form=eventForm)

@app.route('/admin/events/<uuid:id>', methods=['GET'])
@login_required
def admin_myEvents_page(id):
  try:
      attemptedUser = User.findUserById(str(id))
      userEvents = []
      if attemptedUser:
        user_events_id = attemptedUser.events
        for event_id in user_events_id:
          userEvents.append(Events.findEventById(event_id))  
      userEventsTotal = len(userEvents)

      return render_template('adminPages/myEvents.html', userEvents=userEvents, userEventsTotal=userEventsTotal)
  except Exception as e:
   # flash(f'ERRO: {e}', category='danger')
   # return redirect(url_for('home_page'))
   raise


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Você encerrou sua sessão", category="info")
    return redirect(url_for('login_page'))