from app import app


@app.route(
    "/"
)  # decorator, aplicar uma função em cima de outra define que a rota do index é '/'
def index():  # index = nome da página
    return "<b>Hello world!</b>"


# index == '/'
