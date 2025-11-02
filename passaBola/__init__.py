# Importa as bibliotecas e funções necessárias
from flask import Flask
from dotenv import load_dotenv
from os import getenv
from pathlib import Path


# Cria a instância principal da aplicação Flask.
load_dotenv() 
app = Flask(__name__)
cpf_api_key = getenv('CPFHUB_API_KEY') 
secretKey = getenv('FLASK_SECRET_KEY')
app.config['SECRET_KEY'] = secretKey


from passaBola import routes