from flask import Flask

app = Flask(__name__)
# app = instancia do flask, controla toda a aplicação
# __name__ => var especial do interpretador que especificaq o arquivo executado

from app.controllers import default
