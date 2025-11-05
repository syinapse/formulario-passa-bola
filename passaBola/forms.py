from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, EmailField, SubmitField, TextAreaField, DateField, SelectField ,ValidationError, PasswordField
from wtforms.validators import DataRequired, Email, Length
from passaBola.models import Database
from passaBola.brasilApi import getStatesAtTuple
from datetime import datetime, timedelta

states = getStatesAtTuple()

class PlayerForm(FlaskForm):
    data = Database.readDatabase(Database.db_main)

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
        age = int(((currentDate - birthday_to_check.data).days) / 365)
        if age < 16:
            raise ValidationError("Com a data de nascimento inserida, somente jogadoras com mais de 16 anos é permitida.")
    
    cpf = StringField(label="CPF: *", validators=[DataRequired("Informe o seu número de cpf"), Length(min=11, max=11)])
    birthday = DateField(label="Data de nascimento: *", validators=[DataRequired("Informe a sua data de nascimento")])
    full_name = StringField(label="Nome completo: *", validators=[DataRequired("O nome da jogadora deve conter no mínimo 10 caractéres"), Length(min=10, max=50)])
    email = EmailField(label="Email: *", validators=[DataRequired("O campo de email da jogadora não pode estar vazio"), Email("Insira um email válido da jogadora")])
    state = SelectField(label="Estado: *", choices=states, validators=[DataRequired("Escolha um dos estados disponíveis em que a jogadora reside")])
    phone = StringField(label="Celular: *", validators=[DataRequired("Insira um número de celular da jogadora"), Length(min=10, max=12)])
    instagram = StringField(label="Instagram: (Opcional)")
    submit = SubmitField(label="Enviar Inscrição", name="individual")


class TeamForm(FlaskForm):
    data = Database.readDatabase(Database.db_main)

    def validate_players(self, players_to_check = ""):
        if not players_to_check.data:
            raise ValidationError("O campo de jogadoras do clube está vazio! Informe ao menos Uma jogadora")

        lines = players_to_check.data.strip().splitlines()

        if not lines:
            raise ValidationError("Nenhuma jogadora informada. Use uma linha por jogadora.")

        for l in lines:
            try:
                playersSplited = l.split('-')
                cpf = playersSplited[1].strip()

                # Força a formatação do CPF digitado
                if len(cpf) < 10 or len(cpf) > 10 and not cpf.isnumeric():
                    raise ValidationError("O CPF ou separador '-' estão incorretos (ex: Nome - 12345678901).")
            except:
                flash("Algum campo em TIMES foi digitado incorretamente. Tente novamente", category="danger")

    cnpj = StringField(label="CNPJ (Opcional):", validators=[Length(min=0, max=14)])
    team_name = StringField(label="Nome do time: *", validators=[DataRequired("Insira o nome do time de no mínimo 3 caractéres"), Length(min=3, max=50)])
    president_name = StringField(label="Nome do presidente: * ", validators=[DataRequired("Insira o nome do presidente"), Length(min=5, max=50)])
    teamEmail = EmailField(label="Email: *", validators=[DataRequired("O email do time deve ser preenchido"), Email("Insira um email válido do time")])
    teamState = SelectField(label="Estado: *", choices=states, validators=[DataRequired("Insira um estado no campo de Times")])
    teamPhone = StringField(label="Telefone profissional: *", validators=[DataRequired("Insira um telefone profissional ao time"), Length(min=8, max=12)])
    players = TextAreaField(label="Nome e CPF das atletas: *")
    submit = SubmitField(label="Enviar Inscrição",name="teams")

class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired("Campo Obrigatório"), Email("email não cadastrado")])
    password = PasswordField(label="Senha", validators=[DataRequired("Campo Obrigatório")])
    submit = SubmitField(label="Entrar")

class EventForm(FlaskForm):
    data = Database.readDatabase(Database.db_events)

    def validate_title(self, title_to_check: StringField):
        for key in self.data.keys():
            if title_to_check.data == self.data[key]['title']:
                raise ValidationError('O Título do seu evento deve ser único.')

    def validate_event_date_start(self, current_date: DateField):
        if current_date.data <= datetime.now().date():
            raise ValidationError(f"A data do evento não pode ser menor ou igual a data de hoje {datetime.now().strftime('%d/%m/%y')}")
        if current_date.data > datetime.now().date() + timedelta(365*10 + 2):
            raise ValidationError(f'A data do evento não pode começar daqui 10 anos')

    def validate_event_date_end(self, current_date: DateField):
        if current_date.data <= datetime.now().date():
            raise ValidationError(f"A data do evento não pode ser menor ou igual a data de hoje {datetime.now().strftime('%d/%m/%y')}")
        if current_date.data > datetime.now().date() + timedelta(365*10 + 2):
            raise ValidationError(f'A data do evento não pode encerrar daqui 10 anos')
    
    def validate_min_age(self, min_age_check: StringField):
        value = min_age_check.data
        if not value.isnumeric():
            raise ValueError("A idade informada deve ser um número inteiro")
        value = int(value)
        if value > 80 or value < 0:
            raise ValidationError('A idade informada é inválida')
    
    def validate_max_age(self, max_age_check: StringField):
        self.validate_min_age(max_age_check)

    def validate_max_total_uni(self, totals_check: StringField):
        value = totals_check.data
        if not value.isnumeric():
            raise ValueError('O total informado deve ser um número inteiro')
        value = int(value)
        if value > 10000 or value < 0:
            raise ValidationError('O total informado é inválido')
    
    def validate_max_total_team(self, totals_teams_check: StringField):
        self.validate_max_total_uni(totals_teams_check)
    
    def validate_cost_uni(self, cost_uni_check: StringField):
        value = cost_uni_check.data
        if not value.isnumeric():
            raise ValueError('O total informado deve ser um número inteiro')
        value = int(value)

    def validate_cost_team(self, cost_team_check: StringField):
        self.validate_cost_uni(cost_team_check)

    def socialMedia(self, value:str):
        if (not value.startswith('@')):
            value = '@' + value

    title = StringField(label="Título do Evento *", validators=[DataRequired(), Length(min=5, max=30)])
    address = StringField(label="Endereço *", validators=[DataRequired(), Length(max=50)])
    state = SelectField(label="Estado *", choices=states, validators=[DataRequired()])
    event_date_start = DateField(label="Inicio do Evento *", validators=[DataRequired()])
    event_date_end = DateField(label="Final do Evento *", validators=[DataRequired()])
    event_description = TextAreaField(label="Descrição do Evento *", validators=[DataRequired()])
    event_reward = TextAreaField(label='Descrição da Premiação *', validators=[DataRequired()])
    min_age = StringField(label="Idade Mínima", validators=[DataRequired(), Length(max=2)])
    max_age = StringField(label="Idade Máxima", validators=[DataRequired(), Length(max=2)])
    max_total_uni = StringField(label="Total Individual", validators=[DataRequired(), Length(max=5)])
    max_total_team = StringField(label="Total de Time", validators=[DataRequired(), Length(max=5)])
    cost_uni = StringField(label="Taxa Individual: *", validators=[DataRequired(), Length(max=3)])
    cost_team = StringField(label="Taxa por Time: *", validators=[DataRequired()])
    linkedin_link = StringField(label="Linkedin", validators=[Length(max=20)])
    instagram_link = StringField(label="Instagram", validators=[Length(max=20)])
    whatsapp_link = StringField(label="Whatsapp", validators=[Length(max=20)])
    other_link = StringField(label="Outro", validators=[Length(max=20)])

    submit = SubmitField(label="Criar Evento", name="crete-event")