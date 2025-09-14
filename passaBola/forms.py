from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField, DateField, SelectField ,ValidationError
from wtforms.validators import DataRequired, Email, Length
from passaBola.models import Player, Teams, checkCPF
from passaBola.brasilApi import getStatesAtTuple
states = getStatesAtTuple()

class PlayerForm(FlaskForm):
    data = Player.readPlayers()
    def validate_email(self, email_to_check):
        for i in range(len(self.data)):
            if self.data[i]['email'] and self.data[i]['email'] == email_to_check.data:
                raise ValidationError('O email digitado já foi inscrito! Por favor insira outro.')

    def validate_full_name(self, full_name_to_check):
        for i in range(len(self.data)):
            if self.data[i]['full_name'] and self.data[i]['full_name'] == full_name_to_check.data:
                raise ValidationError('O nome inserido já foi inscrito! Por favor insira outro.')   
            
    def validate_cpf(self, cpf_to_check):
        for i in range(len(self.data)):
            if self.data[i]['cpf'] and self.data[i]['cpf'] == cpf_to_check.data:
                raise ValidationError("O CPF inserido já foi inscrito. Por favor insira outro.")
    
    def validate_birthday(self, birthday_to_check):
        from datetime import datetime
        currentDate = datetime.now().date()
        # Checar também com os dados do CPF que foram retornados (colocar em condição OR)
        # O Limite de idade vai depender de evento pra evento, então deve ser pego em uma base de dados o valor quando o usuário cria-lo
        age = int(((currentDate - birthday_to_check.data).days) / 365)
        if age < 16:
            raise ValidationError("Com a data de nascimento inserida, somente jogadoras com mais de 16 anos é permitida.")
    
    cpf = StringField(label="CPF: *", validators=[DataRequired(), Length(min=10, max=10)])
    birthday = DateField(label="Data de nascimento: *", validators=[DataRequired()])
    full_name = StringField(label="Nome completo: *", validators=[DataRequired(), Length(min=10, max=50)])
    email = EmailField(label="Email: *", validators=[DataRequired(), Email()])
    state = SelectField(label="Estado: *", choices=states, validators=[DataRequired()])
    phone = StringField(label="Celular: *", validators=[DataRequired(), Length(min=10, max=12)])
    instagram = StringField(label="Instagram: (Opcional)")
    submit = SubmitField(label="Enviar Inscrição")


class TeamForm(FlaskForm):
    data = Teams.readTeams()

    def validate_players(self, players_to_check):
        lines = players_to_check.data.strip().splitlines()

        if not lines:
            raise ValidationError("Nenhuma jogadora informada. Use uma linha por jogadora.")

        for l in lines:
            try:
                playersSplited = l.split('-')
                cpf = playersSplited[1].strip()

                # Forçando a formatação
                if len(cpf) < 10 or len(cpf) > 10 and not cpf.isnumeric():
                    raise ValidationError("O CPF ou separador '-' estão incorretos (ex: Nome - 12345678901).")
            except:
                raise ValidationError("Algum campo foi digitado incorretamente. Tente novamente")

# temp = players_to_check.data.split('\r\n') for p in temp: if not p: raise Exception() try: playersSplited = p.strip().split(' ') # Forçando a formatação if playersSplited[1] != '-' or len(playersSplited[2]) < 10 or len(playersSplited[2]) > 10 and not playersSplited[2].isnumeric(): raise ValidationError("O CPF ou Nome informado estão incorretos.") except Exception: raise ValidationError("A formatação de jogadoras está incorreta!!")


    cnpj = StringField(label="CNPJ (Opcional):", validators=[DataRequired("Insira o CNPJ"), Length(min=14, max=14)])
    team_name = StringField(label="Nome do time: *", validators=[DataRequired("Insira o nome do time"), Length(min=3, max=50)])
    president_name = StringField(label="Nome do presidente: * ", validators=[DataRequired("Insira o nome do presidente"), Length(min=5, max=50)])
    teamEmail = EmailField(label="Email: *", validators=[DataRequired("O email deve ser preenchido"), Email("Insira um email válido")])
    teamState = SelectField(label="Estado: *", choices=states, validators=[DataRequired("Insira um estado")])
    teamPhone = StringField(label="Telefone profissional: *", validators=[DataRequired("Insira um telefone"), Length(min=8, max=12)])
    players = TextAreaField(label="Nome e CPF das atletas: *")
    submit = SubmitField(label="Enviar Inscrição")
