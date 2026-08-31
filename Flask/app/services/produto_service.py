from app.extensions import db
from app.models.Produto import Produto
from app.models.Categoria import Categoria

class ProdutoService:
    @staticmethod
    def criar_produto(dados):
        categoria_id = dados["categoria_id"]
        categoria_existe = Categoria.query.get(categoria_id)

        if not categoria_existe:
            raise ValueError(f"A categoria com ID {categoria_id} não existe.")
        
        novo_produto = Produto(
            nome=dados["nome"], 
            preco = dados["preco"],
            categoria_id=categoria_id
        )

        db.session.add(novo_produto)
        db.session.commit()

        return novo_produto
    
    @staticmethod
    def listar_produtos():
        return Produto.query.all()