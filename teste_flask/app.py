from flask import Flask

app = Flask(__name__)
# app = instancia do flask, controla toda a aplicação
# __name__ => var especial do interpretador que especificaq o arquivo executado


@app.route("/")  # decorator, aplicar uma função em cima de outra define que a rota do index é '/'
def index():  # index = nome da página
    return "<b>Hello world!</b>"


# index == '/'

if __name__ == "__main__":
    app.run()
