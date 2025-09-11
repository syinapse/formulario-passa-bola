from flask import Flask
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

# path = Path("./../apikeys.env")
load_dotenv()
cpf_api_key = getenv('CPFHUB_API_KEY')
secretKey = getenv('FLASK_SECRET_KEY')
#print("Chave secreta: {0}",secretKey)
app = Flask(__name__)
app.config['SECRET_KEY'] = "fd45c1f731e9c55e46bc062d" # Gerado automaticamente pela função: os.urandom(12).hex()

from passaBola import routes