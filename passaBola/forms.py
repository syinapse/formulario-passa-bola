from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField, DateField, SelectField ,ValidationError
from wtforms.validators import DataRequired, Email, Length
from passaBola.models import Player, Teams, checkCPF
from passaBola.brasilApi import getStatesAtTuple
states = getStatesAtTuple()

class PlayerForm(FlaskForm):
    data = Player.readPlayers()
    print(data[0]['full_name'])
    def validate_email(self, email_to_check):
        for i in range(len(self.data)):
            if self.data[i]['email'] and self.data[i]['email'] == email_to_check.data:
                raise ValidationError('O email digitado já foi cadastrado! Por favor insira outro.')

    def validate_full_name(self, full_name_to_check):
        for i in range(len(self.data)):
            if self.data[i]['full_name'] and self.data[i]['full_name'] == full_name_to_check.data:
                raise ValidationError('O nome inserido já foi cadastrado! Por favor insira outro.')   
            
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
    city = SelectField(label="Cidade: *", choices=states, validators=[DataRequired()])
    phone = StringField(label="Celular: *", validators=[DataRequired(), Length(min=10, max=12)])
    instagram = StringField(label="Instagram: (Opcional)")
    submit = SubmitField(label="Enviar Inscrição")


class TeamForm(FlaskForm):
    cnpj = StringField(label="CNPJ (Opcional):", validators=[DataRequired(), Length(min=14, max=14)])
    team_name = StringField(label="Nome do time: *", validators=[DataRequired(), Length(min=3, max=50)])
    president_name = StringField(label="Nome do presidente: * ", validators=[DataRequired(), Length(min=5, max=50)])
    email = EmailField(label="Email: *", validators=[DataRequired(), Email()])
    city = SelectField(label="Cidade: *", choices=states, validators=[DataRequired()])
    phone = StringField(label="Telefone profissional: *", validators=[DataRequired(), Length(min=8, max=12)])
    players = TextAreaField(label="Nome e CPF das atletas: *", validators=[DataRequired()])
    submit = SubmitField(label="Enviar Inscrição")
