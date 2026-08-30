from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
# app = instancia do flask, controla toda a aplicação
# __name__ => var especial do interpretador que especificaq o arquivo executado
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.controllers import default
