from flask import Blueprint, request, jsonify
from app.services.categoria_service import CategoriaService
from app.schemas.categoria_schema import categoria_schema, categorias_schema
from marshmallow import ValidationError

categoria_bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@categoria_bp.route("/", methods=["POST"])
def criar_categoria():
    json_data = request.get_json()

    try:
        dados_validados = categoria_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400  # retorna mensagem e erro 400

    try:
        nova_categoria = CategoriaService.criar_categoria(dados=dados_validados)
    except ValidationError as err:
        return jsonify({"erro": str(err)}), 404

    resultado = categoria_schema.dump(nova_categoria)
    return jsonify(resultado), 201  # criado com sucesso


@categoria_bp.route("/", methods=["GET"])
def listar_categorias():
    categorias = CategoriaService.listar_categorias()
    resultado = categorias_schema.dump(categorias)

    return jsonify({"categorias": resultado}), 200
