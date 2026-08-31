from app.extensions import db
from app.models.Categoria import Categoria

class CategoriaService:
    @staticmethod
    def criar_categoria(dados):
        nova_categoria = Categoria(nome=dados["nome"])

        db.session.add(nova_categoria) #commita uma nova categoria
        db.session.commit()

        return nova_categoria

    @staticmethod
    def listar_categorias():
        return Categoria.query.all()