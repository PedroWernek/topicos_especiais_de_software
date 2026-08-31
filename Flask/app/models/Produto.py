from app.extensions import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)

    def __repr__(self):
        return f"<Produto {self.nome}>"
