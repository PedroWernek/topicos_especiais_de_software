from flask import Flask
from app.config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.models.Categoria import Categoria
    from app.models.Produto import Produto

    with app.app_context():
        db.create_all()

    from app.routes.produto_routes import produto_bp
    from app.routes.categoria_routes import categoria_bp

    app.register_blueprint(produto_bp)
    app.register_blueprint(categoria_bp)

    return app
