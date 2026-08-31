from flask import Blueprint, request, jsonify
from app.services.produto_service import ProdutoService
from app.schemas.produto_schema import produto_schema, produtos_schema
from marshmallow import ValidationError

produto_bp = Blueprint("produtos", __name__, url_prefix="/produtos")


@produto_bp.route("/", methods=["POST"])
def criar_produto():
    json_data = request.get_json()

    try:
        dados_validados = produto_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        novo_produto = ProdutoService.criar_produto(dados_validados)
    except ValueError as err:
        return jsonify({"erro": str(err)}), 404

    resultado = produto_schema.dump(novo_produto)
    return jsonify(resultado), 201


@produto_bp.route("/", methods=["GET"])
def listar_produtos():
    produtos = ProdutoService.listar_produtos()
    resultado = produtos_schema.dump(produtos)

    return jsonify({"produtos": resultado}), 200
