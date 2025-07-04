from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# --- Inicializando a aplicação
app = Flask(__name__)
app.config.from_pyfile('config.py')

# --- Inserindo Proteção ao Projeto
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

# --- Imports Necessários para Rodar o Projeto
from views import *

# --- Rodando a Aplicação
if __name__ == '__main__':
    app.run(debug=True)