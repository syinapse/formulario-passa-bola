from flask import Flask
from dotenv import load_dotenv
from os import getenv

load_dotenv()
cpf_api_key = getenv('CPFHUB_API_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('FLASK_SECRET_KEY') # Gerado automaticamente pela função: os.urandom(12).hex()

from passaBola import routes