from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "fd45c1f731e9c55e46bc062d" # Gerado automaticamente pela função: os.urandom(12).hex()

from passaBola import routes