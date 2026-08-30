from app import app

@app.route("/index")
@app.route(
    "/"
)  # decorator, aplicar uma função em cima de outra define que a rota do index é "/"
def index():  # index = nome da página
    return "<b>Hello world!</b>"


@app.route("/test", defaults={"name": None})
@app.route("/test/<name>")
def test(name):
    if name:
        return "Hello, %s!" % name
    else:
        return "Hello user!"

@app.route("/id/<int: id>", methods=["GET"])
def test(id):
    if id:
        return f"Hello, {id}!"
    else:
        return "Hello user!"