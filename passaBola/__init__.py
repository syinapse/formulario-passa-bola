# Importa as bibliotecas e funções necessárias
from flask import Flask
from dotenv import load_dotenv
from os import getenv
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from pathlib import Path


# Cria a instância principal da aplicação Flask.
load_dotenv() 
app = Flask(__name__)
secretKey = getenv('FLASK_SECRET_KEY')
cpf_api_key = getenv('CPFHUB_API_KEY') 
app.config['SECRET_KEY'] = secretKey

bcrypt = Bcrypt(app)
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login_page"
loginManager.login_message_category = "info"

from passaBola import routes