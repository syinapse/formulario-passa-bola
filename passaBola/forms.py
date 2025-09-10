from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class PersonForm(FlaskForm):

    # def validate_full_name():
    #    pass

    # def validate_email(self, email_to_check):
    #     data = User.readUsers()
    #     for i in range(len(data)):
    #         if data[i]['email'] == email_to_check.data:
    #             raise ValidationError('Email already exists! Please try a differente email')

    
    full_name = StringField(label="Nome completo: *", validators=[DataRequired(), Length(min=10, max=50)])
    email = EmailField(label="Email: *", validators=[DataRequired(), Email()])
    phone = StringField(label="Celular: *", validators=[DataRequired(), Length(min=10, max=12)])
    instagram = StringField(label="Instagram: (Opcional)")
    submit = SubmitField(label="Enviar Inscrição")


class TeamForm(FlaskForm):
    cnpj = StringField(label="CNPJ (Opcional):", validators=[DataRequired(), Length(min=14, max=14)])
    team_name = StringField(label="Nome do time: *", validators=[DataRequired(), Length(min=3, max=50)])
    president_name = StringField(label="Nome do presidente: * ", validators=[DataRequired(), Length(min=5, max=50)])
    email = EmailField(label="Email: *", validators=[DataRequired(), Email()])
    phone = StringField(label="Telefone profissional: *", validators=[DataRequired(), Length(min=8, max=12)])
    players = TextAreaField(label="Nome e CPF das atletas: *", validators=[DataRequired()])
    submit = SubmitField(label="Enviar Inscrição")
