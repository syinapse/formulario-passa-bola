# Importa as bibliotecas e funções necessárias
from flask import Flask
from dotenv import load_dotenv
from os import getenv
from pathlib import Path


# Cria a instância principal da aplicação Flask.
app = Flask(__name__)
# Configura uma chave secreta para a aplicação.
app.config['SECRET_KEY'] = "fd45c1f731e9c55e46bc062d" # Gerado automaticamente pela função: os.urandom(12).hex()
# path = Path("./../apikeys.env")
load_dotenv() # Executa a função que lê o arquivo .env e carrega suas variáveis no ambiente.
cpf_api_key = getenv('CPFHUB_API_KEY') # Lê o valor da variável de ambiente 'CPFHUB_API_KEY' e o armazena na variável python 'cpf_api_key'.
#secretKey = getenv('FLASK_SECRET_KEY')


# Importa o módulo de rotas da aplicação.
# Este import é colocado no final de propósito para evitar "importações circulares",
from passaBola import routes