# Importa as dependências necessárias do Flask e os módulos da aplicação.
# save this as app.py
from passaBola import app,cpf_api_key
from flask import render_template, flash, redirect, url_for, request
from passaBola.forms import PlayerForm, TeamForm, LoginForm
from passaBola.models import Player, Teams, User
from passaBola.brasilApi import getBrazilStates
from flask_login import login_user, logout_user, login_required

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

@app.route("/event", methods=["GET", "POST"])
def event_page():
     # Instancia os dois formulários que serão usados na página.
    form = PlayerForm(state="")
    teamForm = TeamForm(teamState="")

    # Verifica qual formulário foi enviado pelo usuário (individual ou de times).
    formType = request.form.get('form_type')

    # Lógica para o formulário de inscrição individual.
    if formType == 'individuals':
      # Valida os dados do formulário no envio.
      if form.validate_on_submit():
        # Cria uma nova instância da classe Player com os dados do formulário.
          newPlayer = Player( cpf=form.cpf.data, 
                              birthday=form.birthday.data,
                              full_name=form.full_name.data,
                              state=form.state.data,
                              email=form.email.data.lower(),
                              phone=form.phone.data,
                              instagram=form.instagram.data)
          # Salva a nova jogadora no "banco de dados" JSON.
          newPlayer.witeNewPlayer()
          # Redireciona para a página de conclusão.
          return redirect(url_for("complete_page"))
      
      # Se houver erros de validação, exibe as mensagens para o usuário.
      if form.errors != {}:
          for errors in form.errors.values():
              for e in errors:
                flash(f'{e}', category='danger')  

    # Lógica para o formulário de inscrição de times.
    if formType == 'teams':    
      if teamForm.validate_on_submit():  
          # Cria uma nova instância da classe Teams.
          newTeam = Teams(cnpj=teamForm.cnpj.data,
                          team_name=teamForm.team_name.data,
                          president_name=teamForm.president_name.data,
                          email=teamForm.teamEmail.data.lower(),
                          state=teamForm.teamState.data,
                          phone=teamForm.teamPhone.data)
          
          # Tenta processar a lista de jogadoras inserida no campo de texto.
          try:
            playersList = []
            temp = teamForm.players.data.strip().splitlines()
            # Itera sobre cada linha (cada jogadora) para criar objetos Player.
            for pl in temp:
                split = pl.split('-')
                newPlayer = Player.TeamsPlayers(cpf=split[1].strip(), name=split[0].strip())
                # Adicionando a lista de jogadoras formatadas
                playersList.append(newPlayer)

            # Adiciona a lista de jogadoras ao objeto do time e salva no JSON.
            newTeam.players = playersList
            newTeam.writeTeams()
            return redirect(url_for("complete_page"))
          except Exception:
            flash("Ocorreu um erro enviar o formulário de Times. Confira os campos e tente novamente")

      # Se houver erros de validação no formulário do time, exibe as mensagens.
      if teamForm.errors != {}:
        for errors in teamForm.errors.values():
            for e in errors:
              flash(f'{e}', category='danger')

    # Renderiza o template da página de eventos, passando os dois formulários para o HTML.
    return render_template("event.html", form=form, teamForm=teamForm)

# Define a rota para a página de conclusão/sucesso.
@app.route('/complete')
def complete_page():
    return render_template("complete.html")


@app.route('/admin')
@login_required
def admin_page():
   return render_template('admin.html')


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Você encerrou sua sessão", category="info")
    return redirect(url_for('login_page'))